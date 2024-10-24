import { useState, useEffect } from "react"

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
            <h1>Companies:</h1>
            <h1>Number of Companies applied: {companyNames.length}</h1>
            <ul>
            {companyNames.map((company, index) => (
                <li key={index}>{company}</li>
                ))}
            </ul>
        </div>
    )
}