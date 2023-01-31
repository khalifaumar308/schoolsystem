import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";


export const api = createApi({
    baseQuery : fetchBaseQuery({baseUrl:"http://localhost:8000"}),
    reducerPath: "SMSApi",
    tagTypes : ["User"],
    endpoints : (build) => ({
        getTeachers:build.query({
            query: () => "/account/list_teachers",
            providesTags: ["User"]
        }),
        getStudents:build.query({
            query: () => "/account/list_students",
            providesTags: ["User"]
        }), 
        getParents:build.query({
            query: () => "/account/list_parents",
            providesTags: ["User"]
        }), 
        // Parents Getter
        totalTeacher:build.query({
            query : () => "/account/total_teacher",
            providesTags: ["Parents"]
        }),
        addUser : build.mutation({
            query : (payload) => ({
                url : '/account/register_user',
                method : 'POST',
                body : payload,
                // headers: {
                //     'Content-type' : 'application/json; charset=UTF-8'
                // },
            }),
            invalidatesTags: ["User"]
        }),
        updateTeacher: build.mutation({
            query : ({username, ...payload}) => ({
                url : `/users/teacher/update/${username}/`,
                method : 'POST',
                body : payload,
                headers: {
                    'Content-type' : 'application/json; charset=UTF-8'
                },
            })
        })
    })
})

export const {
    useGetTeachersQuery,
    useTotalTeacherQuery,
    useGetParentsQuery,
    useGetStudentsQuery,

    useAddUserMutation,
    useUpdateTeacherMutation,
    
} = api 