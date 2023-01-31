import { Delete, Edit, Preview } from '@mui/icons-material';
import { Box, IconButton, Tooltip } from '@mui/material';
import React from 'react';


const TeacherDialog = ({params, handleDelete, handleTeacherEdit }) => {
  return (
    <Box>
        <Tooltip title="delete teacher">
            <IconButton onClick={() => handleDelete(params)}>
                <Delete />
            </IconButton>
        </Tooltip>
        <Tooltip title="view teacher">
            <IconButton>
                <Preview />
            </IconButton>
        </Tooltip>
        <Tooltip title="edit teacher">
            <IconButton onClick={()=> handleTeacherEdit(params)}>
                <Edit />
            </IconButton>
        </Tooltip>

    </Box>
  )
}

export default TeacherDialog