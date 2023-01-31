import { LoadingButton } from "@mui/lab";
import {
  Box,
  Dialog,
  DialogContent,
  DialogTitle,
  MenuItem,
  Snackbar,
  TextField,
} from "@mui/material";
import React, { useState } from "react";
import { useEffect } from "react";
import FlexBetween from "scenes/components/FlexBetween";
import { useUpdateTeacherMutation } from "state/api";


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

const EditTeacher = ({ openModal, handleCloseModal, rowId }) => {
  console.log('BEFRERER');
  console.log(rowId, 'lol');
  const [row, setRow] = useState(rowId);
  const [state, setState] = useState("");
  const [country, setCountry] = useState("");

  useEffect(() => {
    if (rowId) {
      setRow(rowId.row.username)
    }
  }, [rowId])
  const [updateTeacher, result] = useUpdateTeacherMutation()
  
  const submitForm = (e) => {
    e.preventDefault();
    let formData = {
      country: country,
      state: state,
    };
    updateTeacher({username: row, ...formData})
      .unwrap()
      .then((data) => console.log(data, 'incorrupt'))
      .then((error) => {
        console.log(error, "errrr");
      });
    };
    
    console.log("🚀 ~ file: EditTeacher.jsx:181 ~ EditTeacher ~ updateTeacher", result)
  const handleStateChange = e => {
    setState(e.target.value)
  }
  return (
    <div>
      <Snackbar />
      <Dialog
        open={openModal}
        onClose={handleCloseModal}
        // autoHideDuration={600}
        sx ={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
        }}
      >
        <DialogTitle id="alert-dialog-title">{"Edit Teacher"}</DialogTitle>
        <DialogContent>
          <form onSubmit={e=>submitForm(e)}>

          <Box
              display="flex"
              alignItems="center"
              width="100%"
              // height="50%"
              m="1rem"
              gap="20px"
              flexDirection="column"
            >
              {/* <FlexBetween gap="20px" width="70%"> */}
                {/* <TextField
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
                 */}
              <FlexBetween>
                <TextField
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
                />
                <TextField
                  required
                  id="filled-required"
                  label="State"
                  defaultValue=""
                  variant="filled"
                  select
                  sx={{
                    gridColumn: "span 2",
                    width: "60%",
                  }}
                  value={state}
                  onChange={e=>handleStateChange(e)}
                >
                  {STATES.map(({ value, label }) => (
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
                Update Teacher
              </LoadingButton>
              </Box>
        </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default EditTeacher;
