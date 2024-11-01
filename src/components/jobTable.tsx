import { useState, useEffect } from "react"
import Table from 'react-bootstrap/Table';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function JobTable(){
    const [companyNames, setCompanyNames] = useState([])

    useEffect(() => {
        fetch("http://localhost:5000/api/companies")
          .then((response) => response.json())
          .then((data) => {
            setCompanyNames(data.companies);
          })
          .catch((error) => {
            console.error("Error fetching companies:", error);
          });
      }, []);

    return (
        <div>
            <h1>Number of Companies: {companyNames.length}</h1>
    
            <Table striped bordered hover variant="dark" className="mt-4"  style={{ fontSize: '2.0rem', width: '100%' }} >
                <thead>
                  <tr>
                    <th></th>
                    <th>Company Name</th>
                    <th>Status</th>
                  </tr>
                </thead>

                <tbody>
                {companyNames.length > 0 ? (
                    companyNames.map((company, index) => (
                      <tr key={index}>
                        <th>{index + 1}</th>
                        <td>{company}</td>
                        <td>{"Sent"}</td>
                      </tr>
                  ))
                 ) : (
                    <tr>
                      <td className="text-center">
                        No companies found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </Table>
        </div>
    )
}