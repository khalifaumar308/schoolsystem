import * as React from "react";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import { useTheme, TextField, MenuItem, Typography } from "@mui/material";
import FlexBetween from "scenes/components/FlexBetween";
import Header from "scenes/components/Header";
// import { width } from "@mui/system";
import { LoadingButton } from "@mui/lab";
import { useState } from "react";
import { useAddClassMutation } from "state/api";
import { useGetTeachersQuery } from "state/api";



export default function AddClass() {
  const theme = useTheme();
  const [name, setName] = useState("");
  const [section, setSection] = useState("");
  const [middleName, setMiddleName] = useState("");
  const [teacher, setTeacher] = useState("");
  const [teacherId, setTeacherId] = useState("");
  const [loadingBtn, setLoadingBtn] = useState(false);
  const [addClass, response] = useAddClassMutation();
  const { data, isloading } = useGetTeachersQuery();
//   console.log("🚀 ~ file: class.jsx:209 ~ AddUser ~ classes", classes)
  // console.log("🚀 ~ file: parents-teacher.jsx:207 ~ AddTeacher ~ data", data);
  // console.log("00000000000000");
  // console.log(parent, "parent");
  const submitForm = (e) => {
    e.preventDefault();
    setLoadingBtn(true)

    const formData = new FormData();
    formData.append("name", name);
    formData.append("section", section);
    formData.append("teacher_id", teacherId);


    console.log(
      "🚀 ~ file: add-teacher.jsx:186 ~ AddTeacher ~ response",
      response
    );

    addClass(formData)
      .unwrap()
      .then(() => setLoadingBtn(false))
      .then((error) => {
        console.log(error, "errrr");
      });
  };
  return (
    <>
      <CssBaseline />
      <Container>
        <Box sx={{ bgcolor: theme.palette.background.alt, height: "80vh" }}>
          <Typography textAlign="center">
            <Header title="Add New User" subTitle="Add User" />
          </Typography>
          <form onSubmit={submitForm}>
            <Box
              display="flex"
              alignItems="center"
              width="100%"
              // height="50%"
              m="1rem"
              gap="20px"
              flexDirection="column"
            >
              <FlexBetween gap="20px" width="70%">
                <TextField
                  required
                  id="filled-required"
                  label="Name"
                  defaultValue=""
                  variant="filled"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                />
                <TextField
                  required
                  id="filled-required"
                  label="Section"
                  defaultValue=""
                  variant="filled"
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                  value={section}
                  onChange={(e) => setSection(e.target.value)}
                />
              
                <TextField
                  // required
                  id="filled-required"
                  label="Teacher"
                  defaultValue=""
                  variant="filled"
                  select
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                  value={teacherId}
                  onChange={(e) => setTeacherId(e.target.value)}
                >
                  {data &&
                    data.map((item) => (
                      <MenuItem key={item.id} value={item.id}>
                        {item.school_user__first_name}{" "}
                        {item.school_user__last_name}
                      </MenuItem>
                    ))}
                </TextField>
                {/* TODO add lga  */}
              </FlexBetween>
            </Box>
            <Box display="flex" justifyContent="center" mt="20px">
              <LoadingButton
                type="submit"
                loading={loadingBtn}
                color="secondary"
                variant="contained"
                className="btn btn-large"
                // onClose={handleCloseModal}
                // onClick={}
                // sx={{
                //  "& .MuiButton-containedSecondary" : {
                //   backgroundColor: "black"
                //  }
                // }}
              >
                Add User
              </LoadingButton>
              {/* <Button color="danger" onClick={handleCloseModal}>Cancel</Button> */}
            </Box>
          </form>
        </Box>
      </Container>
    </>
  );
}
