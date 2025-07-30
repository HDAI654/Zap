"use client";

import { Tab } from "@headlessui/react";
import axios from "axios";
import baseURL, { version } from "@/BaseURL";
import { useEffect, useState } from "react";
import { DataGrid, GridColDef, GridRowsProp } from "@mui/x-data-grid";
import { Button } from "@mui/material";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import { Parser } from "json2csv";

axios.defaults.baseURL = baseURL;
axios.defaults.withCredentials = true;

export default function Panel() {
  const [Tables, setTables] = useState<any[]>([]);
  const [tableData, setTableData] = useState<any[]>([]);
  const [error, setError] = useState(false);
  const [selectedTabIndex, setSelectedTabIndex] = useState<number | null>(null);

  useEffect(() => {
    const getData = async () => {
      try {
        const res = await axios.get(`/api/v${version}/user/tables-names`);
        if (res.data.tables) {
          setTables(res.data.tables);
        }
      } catch {
        setError(true);
      }
    };
    getData();
  }, []);

  const loadTable = async (id: number, index: number) => {
    if (!id || tableData[index]) return;
    try {
      const res = await axios.get(`/api/v${version}/user/tables/${id}`);
      if (res.data.table) {
        const raw = res.data.table.data;
        const keys = Object.keys(raw);
        const rowCount = raw[keys[0]].length;

        const rows: GridRowsProp = Array.from({ length: rowCount }, (_, i) => {
          const row: any = { id: i };
          keys.forEach((key) => {
            row[key] = raw[key][i];
          });
          return row;
        });

        const columns: GridColDef[] = keys.map((key) => ({
          field: key,
          headerName: key,
          width: 150,
          editable: true,
        }));

        const newData = { id, rows, columns };
        console.log(newData);
        setTableData((prev) => {
          const copy = [...prev];
          copy[index] = newData;
          return copy;
        });
      }
    } catch (err) {
      console.error("Load table error:", err);
    }
  };

  const exportCSV = (rows: any[]) => {
    const parser = new Parser();
    const csv = parser.parse(rows);
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "table_export.csv";
    link.click();
  };

  const exportPDF = (rows: any[], columns: any[]) => {
    const doc = new jsPDF();
    doc.text("Table Export", 10, 10);
    autoTable(doc, {
      head: [columns.map((col: any) => col.headerName)],
      body: rows.map((row) => columns.map((col: any) => row[col.field])),
    });
    doc.save("table_export.pdf");
  };

  return (
    <div className="container mt-4">
      <Tab.Group
        selectedIndex={selectedTabIndex ?? -1}
        onChange={(index) => {
          setSelectedTabIndex(index);
          const tbl = Tables[index];
          if (tbl) loadTable(tbl.id, index);
        }}
      >
        <Tab.List className="nav nav-tabs">
          {Tables.map((tbl, index) => (
            <Tab
              key={index}
              className={({ selected }) =>
                `nav-link ${selected ? "active" : ""}`
              }
            >
              {tbl.name}
            </Tab>
          ))}
        </Tab.List>
        {selectedTabIndex !== null && (
          <Tab.Panels className="tab-content p-3 border border-top-0">
            {Tables.map((_, index) => {
              const table = tableData[index];
              return (
                <Tab.Panel key={index}>
                  {table ? (
                    <>
                      <div className="mb-3 flex gap-2">
                        <button
                          className="btn btn-primary"
                          onClick={() => exportCSV(table.rows)}
                        >
                          Export CSV
                        </button>
                        <button
                          className="btn btn-primary mx-5"
                          onClick={() => exportPDF(table.rows, table.columns)}
                        >
                          Export PDF
                        </button>
                      </div>
                      <div style={{ height: 400, width: "100%" }}>
                        <DataGrid
                          rows={table.rows}
                          columns={table.columns}
                          pageSize={5}
                          rowsPerPageOptions={[5, 10, 20]}
                          checkboxSelection
                          disableSelectionOnClick
                          experimentalFeatures={{ newEditingApi: true }}
                        />
                      </div>
                    </>
                  ) : (
                    <div
                      className="d-flex justify-content-center align-items-center"
                      style={{ height: 400 }}
                    >
                      <div className="spinner-border" role="status" />
                    </div>
                  )}
                </Tab.Panel>
              );
            })}
          </Tab.Panels>
        )}
      </Tab.Group>
    </div>
  );
}
