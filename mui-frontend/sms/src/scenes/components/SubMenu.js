import React from "react";
import { useAddEmailMutation } from "state/api";
function SubMenu() {
  let formSubmitError;
  const [addEmail, response] = useAddEmailMutation();
  const [postForm, setPostForm] = React.useState("Submit");

  console.log("new world");
  const onSubmit = (e) => {
    e.preventDefault();
    const {email} = e.target.elements;
    let formData = {
      email: email.value,
    };
    console.log(
      "🚀 ~ file: add-student.jsx:29 ~ onSubmit ~ formData",
      formData,
      "----------",
      response
    );

    addEmail(formData)
      .unwrap()
      .then(() => {})
      .then((error) => {
        console.log(error);
      });
  };
  return (
    <div>
      {formSubmitError}
      <div className="d-flex justify-content-center mb-4">
        <div className="col-md-4 offset-md-*">
          <form onSubmit={onSubmit}>
            <div className="mb-3">
              <label className="form-label">
                <strong>Enter Course Name</strong>
              </label>
              <input type="text" className="form-control" id="email" />
            </div>
            <div className="d-grid">
              <button className="btn btn-danger" type="submit">
                {postForm}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
export default SubMenu;
