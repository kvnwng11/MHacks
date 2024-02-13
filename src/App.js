import React, { useState, useEffect } from "react";
import $ from 'jquery';
import PropTypes from "prop-types";
import { CDBInput, CDBCard, CDBCardBody, CDBIcon, CDBBtn, CDBLink, CDBContainer } from 'cdbreact';
import { MDBDatatable } from 'mdb-react-ui-kit';


import './App.css';
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import "tw-elements-react/dist/css/tw-elements-react.min.css";


import { TEInput, TERipple } from "tw-elements-react";


//Helpful: https://www.freecodecamp.org/news/build-dynamic-forms-in-react/

function App() {
  const [first, setFirst] = useState('');
  const [last, setLast] = useState('');
  const [courses, setCourses] = useState('');

  const submit = (e) => {
    e.preventDefault();
    console.log(first);
    console.log(last);

    const apiUrl = `/api/classes/${first}/${last}/`
    fetch(apiUrl, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // Update state
        setCourses(data);
      })
      .catch((error) => console.log("Error: ", error));
  };

  return (
    <>
      <section className="h-screen">
        <div className="h-full">
          {/* <!-- Left column container with background--> */}
          <div className="g-6 flex h-full flex-wrap justify-center lg:justify-between">
            <div className="shrink-1 mb-12 grow-0 basis-auto md:mb-0 md:w-9/12 md:shrink-0 lg:w-6/12 xl:w-6/12 logo">
              <img
                src="https://tecdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
                className="w-6/12"
                alt="Sample image"
              />
            </div>

            {/* <!-- Right column container --> */}
            <div className="mb-12 md:mb-0 md:w-8/12 lg:w-5/12 xl:w-5/12 enter-name ">
              <form>

                {/* <!-- Separator between social media sign in and email/password sign in --> */}
                <div className="my-4 flex items-center before:mt-0.5 before:flex-1 before:border-t before:border-neutral-300 after:mt-0.5 after:flex-1 after:border-t after:border-neutral-300">
                  <p className="mx-4 mb-0 text-center font-semibold dark:text-white">
                    Enter Your Name
                  </p>
                </div>

                {/* <!-- Email input --> */}
                <TEInput
                  type="text"
                  label="First Name"
                  size="lg"
                  className="mb-6 w-1"
                  onChange={(e) => setFirst(e.target.value)}
                ></TEInput>

                {/* <!--Password input--> */}
                <TEInput
                  type="text"
                  label="Last Name"
                  className="mb-6"
                  size="lg"
                  onChange={(e) => setLast(e.target.value)}
                ></TEInput>

                {/* <!-- Login button --> */}
                <div className="text-center lg:text-left">
                  <TERipple rippleColor="light">
                    <button
                      type="button"
                      className="inline-block rounded bg-primary px-7 pb-2.5 pt-3 text-sm font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
                      onClick={submit}
                    >
                      Submit
                    </button>
                  </TERipple>
                </div>
              </form>
            </div>
          </div>
        </div>
      </section>

      <div className="results-table">


        <table className="table table-hover">
          <thead>
            <tr>
              <th>#</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Expected Grade</th>
              <th>Expected Engagement</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">1</th>
              <td>Mark</td>
              <td>Otto</td>
              <td>3.8</td>
              <td>80%</td>
            </tr>
            <tr>
              <th scope="row">2</th>
              <td>Jacob</td>
              <td>Thornton</td>
              <td>3.9</td>
              <td>90%</td>
            </tr>
          </tbody>
        </table>
      </div>


    </>
  );
}

export default App;
