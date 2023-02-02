import { CssBaseline, ThemeProvider } from "@mui/material";
import { createTheme } from "@mui/material/styles";
import { themeSettings } from "theme";
import React, { useMemo } from "react";
import { useSelector } from "react-redux";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Dashboard from "scenes/dashboard";
import Layout from "scenes/layout";
import ListTeachers from "scenes/teachers";
import ListStudents from "scenes/students";
// import AddTeacher from "scenes/teachers/add-teacher";
import AddUser from "scenes/users/add-user";
import AddClass from "scenes/classes/add-class";

function App() {
  const mode = useSelector((state) => state.global.mode);
  const theme = useMemo(() => createTheme(themeSettings(mode), [mode]));
  return (
    <div className="app">
      <BrowserRouter>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Routes>
            <Route element={<Layout />}>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/list-teachers" element={<ListTeachers />} />
              <Route path="/list-students" element={<ListStudents />} />
              <Route path="/add-user" element={<AddUser />} />
              <Route path="/add-class" element={<AddClass />} />
              <Route path="/breakdown" element={"Break"} />

            </Route>
          </Routes>
        </ThemeProvider>
      </BrowserRouter>
    </div>
  );
};

export default App; 