"use client";

import { Tab } from "@headlessui/react";
import axios from "axios";
import baseURL, { version } from "@/BaseURL";
import { useEffect, useState, useRef } from "react";
import { DataGrid, GridColDef, GridRowsProp } from "@mui/x-data-grid";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import { Parser } from "json2csv";
import TableView from "@/components/tableView";
import VoiceRec from "@/components/voiceRec";

axios.defaults.baseURL = baseURL;
axios.defaults.withCredentials = true;

export default function Panel() {
  const [Tables, setTables] = useState<any[]>([]);
  const [tableData, setTableData] = useState<any[]>([]);
  const [error, setError] = useState(false);
  const [selectedTabIndex, setSelectedTabIndex] = useState<number | null>(null);
  const [selectedRows, setSelectedRows] = useState<any[]>([]);

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
        const name = res.data.table.name;
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
        }));

        const newData = { id, name, rows, columns };
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

  return (
    <div className="container mt-4">
      <VoiceRec />
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
                      <div style={{ height: "500px", width: "100%" }}>
                        <TableView tblData={table} />
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
