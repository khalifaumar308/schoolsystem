// import React from "react";
// import {
//   Drawer,
//   List,
//   ListItem,
//   ListItemIcon,
//   ListItemText,
//   Collapse,
//   useTheme
// } from "@mui/material";

import React from 'react'

const SideBar = () => {
  return (
    <div>SideBar</div>
  )
}

export default SideBar

// import {makeStyles} from "@mui/styles";
// import { DashboardOutlined as DashboardIcon } from "@mui/icons-material";
// import { SchoolOutlined as SchoolIcon } from "@mui/icons-material";
// import { AssignmentIndOutlined as AssignmentIcon } from "@mui/icons-material";
// import { ExpandMore, ExpandLess } from "@mui/icons-material";


// const useStyles = makeStyles({
//   list: {
//     width: 250,
//   },
// });

// export default function Sidebar({
//     drawerWidth,
//     isNonMobile
// }) {
//   const classes = useStyles();
//   const [open, setOpen] = React.useState(false);
//   const [teacherOpen, setTeacherOpen] = React.useState(false);
//   const theme = useTheme();

//   const handleClick = () => {
//     setTeacherOpen(!teacherOpen);
//   };


//   <Drawer 
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

//   return (
//     <Drawer variant="permanent" anchor="left"
//         sx={{
//             width: drawerWidth,
//             "& .MuiDrawer-paper": {
//             color: "gray",
//             backgroundColor: "red",
//             border: "2px solid red",
//             boxSizing: "border-box",
//             borderWidth: isNonMobile ? 0 : "2px",
//             width: drawerWidth,
//             },
//         }}
//     >
//       <List className={classes.list}>
//         <ListItem button>
//           <ListItemIcon>
//             <DashboardIcon />
//           </ListItemIcon>
//           <ListItemText primary="Dashboard" />
//         </ListItem>
//         <ListItem button onClick={handleClick}>
//           <ListItemIcon>
//             <SchoolIcon />
//           </ListItemIcon>
//           <ListItemText primary="Teacher" />
//           {teacherOpen ? <ExpandLess /> : <ExpandMore />}
//         </ListItem>
//         <Collapse in={teacherOpen} timeout="auto" unmountOnExit>
//           <List component="div" disablePadding>
//             <ListItem button className={classes.nested}>
//               <ListItemText primary="Add Teacher" />
//             </ListItem>
//             <ListItem button className={classes.nested}>
//               <ListItemText primary="List Teachers" />
//             </ListItem>
//           </List>
//         </Collapse>
//         <ListItem button>
//           <ListItemIcon>
//             <AssignmentIcon />
//           </ListItemIcon>
//           <ListItemText primary="Grades" />
//         </ListItem>
//       </List>

//     </Drawer>
//   );
// }


{/* <Collapse in={activeSubMenu === text} timeout="auto" unmountOnExit>
                      {children.map (({text : subText, icon: subIcon}) => {
                        const subLcText = subText.toLowerCase();
                        return (
                            <ListItem key={subText} disablePadding>
                                <ListItemButton onClick={()=> {
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
                                        p: "0 2.5rem 0 "
                                  }}>
                                    <ListItemIcon
                                    sx={{
                                        ml:"2rem",
                                        color : 
                                        active === subLcText
                                            ? theme.palette.primary[600]
                                            : theme.palette.secondary[200]
                                    }}
                                    >

                                    {subIcon}
                                    </ListItemIcon>
                                    <ListItemText primary={subLcText} />
                                    {active === subLcText && (
                                        <ChevronRightOutlined sx={{ ml: "auto" }} />
                                    )}

                                  </ListItemButton>
                            </ListItem>
                        )
                      })}
                      </Collapse> */}
                      
                      {/* <ListItemButton
                       
                        onClick={() => {
                          if (activeSubMenu === text) {
                            setActiveSubMenu(null);
                          } else {
                            setActiveSubMenu(text);
                          }
                        }}
                      >
                      </ListItemButton>
                       */}