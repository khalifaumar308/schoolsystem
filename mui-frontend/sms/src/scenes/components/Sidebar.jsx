import React, { useState, useEffect } from "react";
import {
  Box,
  Divider,
  List,
  IconButton,
  Drawer,
  ListItem,
  Typography,
  useTheme,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Collapse,
} from "@mui/material";

import {
  SettingsOutlined,
  ChevronLeft,
  ChevronRightOutlined,
  HomeOutlined,
  TodayOutlined,
  CalendarMonthOutlined,
  AdminPanelSettingsOutlined,
  PieChartOutline,
  Groups2Outlined,
  PublicOutlined,
  TrendingUpOutlined,
  AddCircleOutline,
  VerifiedUserRounded,
  PeopleOutline,
  ChevronLeftRounded,
  ExpandMore,
  ExpandLess,
  PlusOneOutlined,
  ClassOutlined,
} from "@mui/icons-material";

import { useLocation, useNavigate } from "react-router-dom";
import FlexBetween from "./FlexBetween";

const navItems = [
  {
    text: "Dashboard",
    icon: <HomeOutlined />,
  },
  {
    text: "Teachers Page",
    icon: null,
  },
  {
    text: "List-Teachers",
    icon: <PeopleOutline />,
    children: [
      // {
      //   text: "List-Teachers",
      //   icon: <VerifiedUserRounded />,
      // },
      {
        text: "Add-Teacher",
        icon: <AddCircleOutline />,
      },
    ],
  },
  {
    text: "Staff Page",
    icon: null,
  },
  {
    text: "List-Staffs",
    icon: <PeopleOutline />,
    children: [
      // {
      //   text: "List-Teachers",
      //   icon: <VerifiedUserRounded />,
      // },
      {
        text: "Add-Staff",
        icon: <AddCircleOutline />,
      },
    ],
  },
  {
    text: "Student Page",
    icon: null,
  },
  {
    text: "List-Students",
    icon: <PeopleOutline />,
    children: [
      // {
      //   text: "List-Teachers",
      //   icon: <VerifiedUserRounded />,
      // },
      {
        text: "Add-Student",
        icon: <AddCircleOutline />,
      },
    ],
  },

  {
    text: "Others",
    icon: null,
  },
  {
    text: "Monthly",
    icon: <CalendarMonthOutlined />,
  },
  {
    text: "Breakdown",
    icon: <PieChartOutline />,
  },
  {
    text: "Add-User",
    icon: <PlusOneOutlined />,
  },
  {
    text: "Add-Class",
    icon: <ClassOutlined />,
  },
  
];

// function Sidebar({ isSidebarOpen, setIsSidebarOpen }) {
//   return (
//     <Drawer
//         open={isSidebarOpen}
//         onClose={() => setIsSidebarOpen(false)}
//     >
//       <List>
//         {navItems.map((item, index) => (
//           <React.Fragment key={index}>
//             <ListItem button>
//               <ListItemIcon>{item.icon}</ListItemIcon>
//               <ListItemText primary={item.text} />
//             </ListItem>
//             {item.children && (
//               <List>
//                 {item.children.map((child, childIndex) => (
//                   <ListItem button key={childIndex}>
//                     <ListItemIcon>{child.icon}</ListItemIcon>
//                     <ListItemText primary={child.text} />
//                   </ListItem>
//                 ))}
//               </List>
//             )}
//           </React.Fragment>
//         ))}
//       </List>
//     </Drawer>
//   );
// }

const Sidebar = ({
  isSidebarOpen,
  setIsSidebarOpen,
  drawerWidth,
  isNonMobile,
}) => {
  const { pathname } = useLocation();
  const [active, setActive] = useState("");
  const [open, setOpen] = useState(false);
  const [activeSubMenu, setActiveSubMenu] = useState(null);
  const navigate = useNavigate();
  const theme = useTheme();

  useEffect(() => {
    setActive(pathname.substring(1));
  }, [pathname]);

  const handleOpen = () => {
    setOpen(!open);
  };

  return (
    <Box component="nav">
      {isSidebarOpen && (
        <Drawer
          open={isSidebarOpen}
          onClose={() => setIsSidebarOpen(false)}
          variant="persistent"
          anchor="left"
          sx={{
            width: drawerWidth,
            "& .MuiDrawer-paper": {
              color: theme.palette.secondary,
              backgroundColor: theme.palette.background.alt,
              boxSizing: "border-box",
              borderWidth: isNonMobile ? 0 : "2px",
              width: drawerWidth,
            },
          }}
        >
          <Box width="100%">
            <Box m="1.5rem 2rem 2rem 3rem">
              <FlexBetween color={theme.palette.secondary.main}>
                <Box display="flex" alignItems="center" gap="0.5rem">
                  <Typography variant="h4" fontWeight="bold">
                    SMS
                  </Typography>
                </Box>
                {!isNonMobile && (
                  <IconButton onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
                    <ChevronLeft />
                  </IconButton>
                )}
              </FlexBetween>
            </Box>
            <List>
              {navItems.map(({ text, icon, children }) => {
                if (!icon) {
                  return (
                    <Typography
                      variant="h6"
                      fontWeight="bold"
                      key={text}
                      sx={{ m: ".5rem 0 1rem 3rem" }}
                    >
                      {text}
                    </Typography>
                  );
                }

                const lcText = text.toLowerCase();
                return (
                  <>
                    <ListItem key={text} disablePadding divider>
                      <ListItemButton
                        onClick={() => {
                          navigate(`/${lcText}`);
                          setActive(lcText);
                          handleOpen();
                        }}
                        sx={{
                          backgroundColor:
                            active === lcText
                              ? theme.palette.secondary[300]
                              : "transparent",
                          color:
                            active === lcText
                              ? theme.palette.primary[600]
                              : theme.palette.secondary[100],
                        }}
                      >
                        <ListItemIcon
                          sx={{
                            ml: "2rem",
                            color:
                              active === lcText
                                ? theme.palette.primary[600]
                                : theme.palette.secondary[200],
                          }}
                        >
                          {icon}
                        </ListItemIcon>
                        <ListItemText primary={text} />
                        {children ? (
                          active === lcText &&
                          (open ? (
                            <ExpandMore sx={{ ml: "auto" }} />
                          ) : (
                            <ChevronRightOutlined sx={{ ml: "auto" }} />
                          ))
                        ): (
                          <>
                            <ChevronRightOutlined sx={{ ml : "auto" }} />
                          </>
                        )}
                      </ListItemButton>
                    </ListItem>
                    {active == lcText && (
                      <Collapse in={open} timeout="auto" unmountOnExit>
                        <ListItem>
                          {children &&
                            children.map(({ text: subText, icon: subIcon }) =>{
                              const subLcText = subText.toLowerCase();
                              return (
                              <ListItemButton
                                // sx={{ pl: 4 }}
                                onClick={() => {
                                  navigate(`/${subLcText}`);
                                  setActive(subLcText);
                                }}
                                sx={{
                                  backgroundColor:
                                    active === subLcText
                                      ? theme.palette.secondary[300]
                                      : "transparent",
                                  color:
                                    active === subLcText
                                      ? theme.palette.primary[600]
                                      : theme.palette.secondary[100],
                                }}
                              >
                                <ListItemIcon
                                  sx={{
                                    ml: "2rem",
                                    color:
                                      active === subLcText
                                        ? theme.palette.primary[600]
                                        : theme.palette.secondary[200],
                                  }}
                                >{subIcon}</ListItemIcon>
                                <ListItemText primary={subLcText} />
                              </ListItemButton>
                            )})}
                        </ListItem>
                      </Collapse>
                    )}
                  </>
                );
              })}
            </List>
          </Box>
        </Drawer>
      )}
    </Box>
  );
};

export default Sidebar;
