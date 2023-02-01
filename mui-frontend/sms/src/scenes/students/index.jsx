import React, { useState } from "react";
import { Box, useTheme } from "@mui/material";
import { useGetStudentsQuery } from "state/api";
import Header from "scenes/components/Header";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import TeacherDialog from "./TeacherDialog";
import EditTeacher from "./EditTeacher";

const ListStudents = () => {
  const [openModal, setOpenModal] = useState(false)
  const [rowId, setRowId] = useState("")
  const theme = useTheme();
  const { data, isLoading, isError } = useGetStudentsQuery();
  // console.log("🚀 ~ file: index.js:10 ~ ListStudents ~ useGetTeachersQuery", useGetTeachersQuery)
  console.log(data, "teacher", isLoading, isError);


  const handleCloseModal = () => {
    setOpenModal(false)
  }
  const handleClickModal = () => {
    setOpenModal(true);
  };

  const columns = [
    {
      field: "id",
      headerName: "ID",
      flex: 1,
      hide: true,
    },
    {
      field: "index",
      headerName: "S/N",
      flex: 1,
      renderCell: (index) => index.api.getRowIndex(index.row.id) + 1,
      // hide : true
    },
    {
      field: "school_user__first_name",
      headerName: "FirstName",
      flex: 1,
    },
    {
      field: "school_user__last_name",
      headerName: "LastName",
      flex: 1,
    },
    {
      field: "school_user__email",
      headerName: "email",
      flex: 1,
      // minWidth:400,
    },
    {
      field: "username",
      headerName: "UserName",
      flex: 1,
    },
    {
      field: "state",
      headerName: "State",
      flex: 1,
    },
    {
      field: "actions",
      headerName: "Actions",
      type: "actions",
      width: 150,
      renderCell : (params) => <TeacherDialog {...{params, handleTeacherEdit, handleDelete}} />
    },
    // TODO : add date of resumption
  ];

  const handleTeacherEdit = async (param) => {
    console.log("PARAMS")
    console.log(param.row.username)
    setRowId(await param)
    handleClickModal()
    console.log('i habver', rowId)
  }

  const handleDelete = async (param) => {
    console.log("DELETE PROPS")
    console.log("I Clicked delete")
  }

  return (
    <>
      <Box m="1.5rem 2.5rem">
        <Header title="All Students" subTitle="List of Students" />
        <Box
          mt="40px"
          height="75vh"
          sx={{
            "& .MuiDataGrid-root": {
              border: "none",
            },
            "& .MuiDataGrid-cell": {
              borderBottom: "none",
            },
            "& .MuiDataGrid-columnHeaders": {
              backgroundColor: theme.palette.background.alt,
              color: theme.palette.secondary[100],
              borderBottom: "none",
            },
            "& .MuiDataGrid-virtualScroller": {
              backgroundColor: theme.palette.primary.light,
            },
            "& .MuiDataGrid-footerContainer": {
              backgroundColor: theme.palette.background.alt,
              color: theme.palette.secondary[100],
              borderTop: "none",
            },
            "& .MuiDataGrid-toobarContainer .MuiButton-text": {
              color: `${theme.palette.secondary[200]} !important`,
              // borderBottom: "none"
            },
          }}
        >
          <DataGrid
            rows={data || []}
            loading={isLoading || !data}
            error={isError}
            getRowId={(row) => row.id}
            columns={columns}
            components={{ Toolbar: GridToolbar }}
            componentsProps={{
              toolbar: {
                showQuickFilter: true,
                quickFilterProps: { debounceMs: 500 },
              },
            }}
          />
        </Box>
        <EditTeacher openModal={openModal} handleCloseModal={handleCloseModal} rowId={rowId} />
      </Box>
    </>
  );
};

export default ListStudents;
