import * as React from "react";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import { useTheme, TextField, MenuItem } from "@mui/material";
import FlexBetween from "scenes/components/FlexBetween";
import Header from "scenes/components/Header";
// import { width } from "@mui/system";
import { LoadingButton } from "@mui/lab";
import { useState } from "react";
import { useAddTeacherMutation } from "state/api";
import { useGetParentsQuery } from "state/api";

const ROLES = [
  {
    value: "Teacher",
    label: "Teacher",
  },
  {
    value: "Student",
    label: "Student",
  },
  {
    value: "Parent",
    label: "Parent",
  },
];

const GENDER = [
  {
    value: "Male",
    label: "Male",
  },
  {
    value: "Female",
    label: "Female",
  },
 
];


const STATES = [
  {
    value: "ABIA",
    label: "Abia",
  },
  {
    value: "ADAMAWA",
    label: "Adamawa",
  },
  {
    value: "AKWA-IBOM",
    label: "AkwaIbom",
  },
  {
    value: "ANAMBRA",
    label: "Anambra",
  },
  {
    value: "BAUCHI",
    label: "Bauchi",
  },
  {
    value: "BAYELSA",
    label: "Bayelsa",
  },
  {
    value: "BENUE",
    label: "Benue",
  },
  {
    value: "BORNO",
    label: "Borno",
  },
  {
    value: "CROSS-RIVER",
    label: "CrossRiver",
  },
  {
    value: "DELTA",
    label: "Delta",
  },
  {
    value: "EBONYI",
    label: "Ebonyi",
  },
  {
    value: "EDO",
    label: "Edo",
  },
  {
    value: "EKITI",
    label: "Ekiti",
  },
  {
    value: "ENUGU",
    label: "Enugu",
  },
  {
    value: "GOMBE",
    label: "Gombe",
  },
  {
    value: "IMO",
    label: "Imo",
  },
  {
    value: "JIGAWA",
    label: "Jigawa",
  },
  {
    value: "KADUNA",
    label: "Kaduna",
  },
  {
    value: "KANO",
    label: "Kano",
  },
  {
    value: "KATSINA",
    label: "Katsina",
  },
  {
    value: "KEBBI",
    label: "Kebbi",
  },
  {
    value: "KOGI",
    label: "Kogi",
  },
  {
    value: "KWARA",
    label: "Kwara",
  },
  {
    value: "LAGOS",
    label: "Lagos",
  },
  {
    value: "NASSARAWA",
    label: "Nassarawa",
  },
  {
    value: "NIGER",
    label: "Niger",
  },
  {
    value: "OGUN",
    label: "Ogun",
  },
  {
    value: "ONDO",
    label: "Ondo",
  },
  {
    value: "OSUN",
    label: "Osun",
  },
  {
    value: "OYO",
    label: "Oyo",
  },
  {
    value: "PLATEAU",
    label: "Plateau",
  },
  {
    value: "RIVERS",
    label: "Rivers",
  },
  {
    value: "SOKOTO",
    label: "Sokoto",
  },
  {
    value: "TARABA",
    label: "Taraba",
  },
  {
    value: "YOBE",
    label: "Yobe",
  },
  {
    value: "ZAMFARA",
    label: "Zamfara",
  },
  {
    value: "FCT-ABUJA",
    label: "FctAbuja",
  },
];

export default function AddTeacher() {
  const theme = useTheme();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [middleName, setMiddleName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");
  const [gender, setGender] = useState("");
  const [parent, setParent] = useState("");
  // const [country, setCountry] = useState("");
  // const [state, setState] = useState("");
  // const [firstName, setFirstName] = useState("")
  const [addTeacher, response] = useAddTeacherMutation();
  const {data, isloading} = useGetParentsQuery()
  console.log("🚀 ~ file: parents-teacher.jsx:207 ~ AddTeacher ~ data", data)
  console.log("00000000000000")
    console.log(parent, 'parent')
  const submitForm = (e) => {
    e.preventDefault();
    // let formData = {
    //   first_name: firstName,
    //   last_name: lastName,
    //   middle_name: middleName,
    //   email: email,
    //   roles: role,
    //   gender: gender,
    //   // country: country,
    //   // state: state,
    // };
    
    const formData = new FormData();
    formData.append("first_name", firstName)
    formData.append("last_name", lastName)
    formData.append("middle_name", middleName)
    formData.append("email", email)
    formData.append("gender", gender)
    formData.append("roles", role)
    formData.append("parent_id", parent)
    console.log(
      "🚀 ~ file: add-teacher.jsx:198 ~ submitForm ~ formData",
      formData.get("email")
    );

    console.log(
      "🚀 ~ file: add-teacher.jsx:186 ~ AddTeacher ~ response",
      response
    );

    addTeacher(formData)
      .unwrap()
      .then(() => {})
      .then((error) => {
        console.log(error, "errrr");
      });
  };
  return (
    <>
      <CssBaseline />
      <Container>
        <Box sx={{ bgcolor: theme.palette.background.alt, height: "80vh" }}>
          <Header title="Add New Teacher" subTitle="add Teacher" />
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
                  label="First Name"
                  defaultValue=""
                  variant="filled"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                />
                <TextField
                  required
                  id="filled-required"
                  label="Last Name"
                  defaultValue=""
                  variant="filled"
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                />
                <TextField
                  required
                  id="filled-required"
                  label="Middle Name"
                  defaultValue=""
                  variant="filled"
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                  value={middleName}
                  onChange={(e) => setMiddleName(e.target.value)}
                />
              </FlexBetween>

              <FlexBetween gap="20px" width="70%">
                <TextField
                  required
                  id="filled-required"
                  label="Email"
                  defaultValue=""
                  variant="filled"
                  type="email"
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <TextField
                  required
                  id="filled-required"
                  label="Role"
                  defaultValue=""
                  variant="filled"
                  select
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                >
                  {ROLES.map(({ value, label }) => (
                    <MenuItem key={value} value={value}>
                      {label}
                    </MenuItem>
                  ))}
                </TextField>
                <TextField
                  // required
                  id="filled-required"
                  label="Parent"
                  defaultValue=""
                  variant="filled"
                  select
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                  value={parent}
                  onChange={(e) => setParent(e.target.value)}
                >
                  {data && 
                    data.map(item => (
                    <MenuItem key={item.id} value={item.id}>
                      {item.school_user__first_name} {item.school_user__last_name}
                    </MenuItem>
                  ))}
                </TextField>
                {/* <TextField
                  required
                  id="filled-required"
                  label="Country"
                  defaultValue=""
                  variant="filled"
                  //  make select later
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                  value={country}
                  onChange={(e) => setCountry(e.target.value)}
                /> */}
                <TextField
                  required
                  id="filled-required"
                  label="Gender"
                  defaultValue=""
                  variant="filled"
                  select
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                >
                  {GENDER.map(({ value, label }) => (
                    <MenuItem key={value} value={value}>
                      {label}
                    </MenuItem>
                  ))}
                </TextField>

                {/* TODO add lga  */}
              </FlexBetween>
            </Box>
            <Box display="flex" justifyContent="center" mt="20px">
              <LoadingButton
                type="submit"
                // loading={loadingBtn}
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
                Add Teacher
              </LoadingButton>
              {/* <Button color="danger" onClick={handleCloseModal}>Cancel</Button> */}
            </Box>
          </form>
        </Box>
      </Container>
    </>
  );
}
