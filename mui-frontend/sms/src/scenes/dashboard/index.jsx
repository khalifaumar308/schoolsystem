import React, { useState, useEffect } from "react";
import Header from "scenes/components/Header";
import FlexBetween from "scenes/components/FlexBetween";
import { Box, Button, useMediaQuery, useTheme } from "@mui/material";
import {
  DownloadOutlined,
  MoneyOutlined,
  PeopleAltTwoTone,
  PeopleOutlineOutlined,
} from "@mui/icons-material";
import StatBox from "scenes/components/StatBox";
import { useTotalTeacherQuery } from "state/api";
import { io } from "socket.io-client";

const Dashboard = () => {
  // TODO : getting live updated data from django
  // const [total, setTotal] = useState()
  // const socket = io("http://localhost:8080");
  // console.log("🚀 ~ file: index.jsx:18 ~ Dashboard ~ socket", socket)

  const theme = useTheme();
  const isNonMediumScreen = useMediaQuery("(min-width: 1200px)");

  const { data, loading } = useTotalTeacherQuery();
  // useEffect(() => {
  //   socket.on('/users/total_teachers', totalTeachers => {
  //     setTotal(totalTeachers)
  //   });
  //   return () => {
  //     socket.off('/users/total_teachers')
  //   }
  // }, [])

  // console.log('total : ', total );

  console.log(data, "loool", loading);

  return (
    <Box m="1.5rem 2.5rem">
      <FlexBetween>
        <Header title="DASHBOARD" subTitle="Welcome to your Dashboard" />
        <Box>
          <Button
            sx={{
              backgroundColor: theme.palette.secondary.light,
              color: theme.palette.background.alt,
              fontSize: "14px",
              fontWeight: "bold",
              padding: "10px 20px",
            }}
          >
            <DownloadOutlined sx={{ mr: "10px" }} />
            Download Reports
          </Button>
        </Box>
      </FlexBetween>
      <Box
        mt="20px"
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="160px"
        gap="20px"
        sx={{
          "& > div": { gridColumn: isNonMediumScreen ? undefined : "span 12" },
        }}
      >
        <StatBox
          title="Total Teachers"
          value={data && data.total}
          increase={`+${data && data.month - data.today}%`}
          description="since last month"
          icon={
            <PeopleAltTwoTone
              sx={{ color: theme.palette.secondary[300], fontSize: "46px" }}
            />
          }
        />

        <StatBox
          title="Total Student"
          value="14000"
          increase="+14%"
          description="since last month"
          icon={
            <PeopleOutlineOutlined
              sx={{ color: theme.palette.secondary[300], fontSize: "46px" }}
            />
          }
        />

        <StatBox
          title="Total Parents"
          value="14000"
          increase="+14%"
          description="since last month"
          icon={
            <PeopleOutlineOutlined
              sx={{ color: theme.palette.secondary[300], fontSize: "46px" }}
            />
          }
        />

        <StatBox
          title="Total Earnings"
          value="14000"
          increase="+14%"
          description="since last month"
          icon={
            <MoneyOutlined
              sx={{ color: theme.palette.secondary[300], fontSize: "46px" }}
            />
          }
        />
      </Box>
    </Box>
  );
};

export default Dashboard;
