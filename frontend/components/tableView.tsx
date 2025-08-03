"use client";

import { useEffect, useState, useRef } from "react";
import { DataGrid, GridColDef, GridRowsProp } from "@mui/x-data-grid";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import { Parser } from "json2csv";

export default function TableView({ tblData }: { tblData: any }) {
  const [selectedRows, setSelectedRows] = useState<any[]>([]);
  const [data, setData] = useState(tblData);

  const addRow = () => {
    setData((prev: any) => {
      const newData = JSON.parse(JSON.stringify(prev));

      const existingIds = newData.rows.map((r: any) => r.id);
      const maxId = existingIds.length > 0 ? Math.max(...existingIds) : 0;
      const newId = maxId + 1;

      const newRow: any = { id: newId };
      newData.columns.forEach((col: any) => {
        newRow[col.field] = "";
      });

      return {
        ...newData,
        rows: [...newData.rows, newRow],
      };
    });
  };

  const exportCSV = () => {
    try {
      const parser = new Parser();
      const csv = parser.parse(data.rows);
      const blob = new Blob([csv], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${data.name}_export.csv`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error exporting CSV:", error);
    }
  };

  const exportPDF = () => {
    try {
      const doc = new jsPDF();
      doc.text(`${data.name} Export`, 10, 10);
      autoTable(doc, {
        head: [data.columns.map((col) => col.field)],
        body: data.rows.map((row) =>
          data.columns.map((col) => row[col.field] ?? "")
        ),
      });
      doc.save(`${data.name}_export.pdf`);
    } catch (error) {
      console.error("Error exporting PDF:", error);
    }
  };

  const deleteRows = () => {
    if (selectedRows.length === 0) return;

    setData((prev) => ({
      ...prev,
      rows: prev.rows.filter((row) => !selectedRows.includes(row.id)),
    }));
    setSelectedRows([]);
  };

  return (
    <>
      <div className="mb-3 d-flex">
        <button className="btn btn-success me-2" onClick={addRow}>
          <i className="fas fa-plus"></i>
        </button>
        {data.columns.length !== 0 && data.rows.length !== 0 && (
          <>
            <button className="btn btn-primary me-2" onClick={exportCSV}>
              <i className="fas fa-file-csv"></i>
            </button>

            <button className="btn btn-primary me-2" onClick={exportPDF}>
              <i className="fas fa-file-pdf"></i>
            </button>

            {selectedRows.length !== 0 && (
              <button className="btn btn-danger me-2" onClick={deleteRows}>
                <i className="fas fa-trash"></i>
              </button>
            )}
          </>
        )}
      </div>

      <DataGrid
        rows={data.rows}
        className="w-100"
        style={{ height: "90%" }}
        columns={data.columns.map((col: any) => ({
          ...col,
          editable: true,
        }))}
        pageSize={5}
        editMode="cell"
        rowsPerPageOptions={[5, 10, 20]}
        checkboxSelection
        disableSelectionOnClick
        experimentalFeatures={{ newEditingApi: true }}
        onRowSelectionModelChange={(newSelectionModel) => {
          const ids = Array.from(newSelectionModel?.ids ?? []);
          setSelectedRows(ids);
        }}
      />
    </>
  );
}
