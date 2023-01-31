import React from 'react';
import {Typography, Box, } from "@mui/material"

const Header = ({title, subTitle}) => {
  return (
    <Box>
        <Typography variant="h2"
        fontWeight="bold"
        color="#3f3"
        sx={{
            mb:"5px"
        }}
        >
            {title}

        </Typography>

        <Typography variant="h5"
        color="#3ff"
        sx={{
            mb:"5px"
        }}
        >
            {subTitle}

        </Typography>
    </Box>
  )
}

export default Header