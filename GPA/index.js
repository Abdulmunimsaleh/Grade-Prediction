async function predictGPA(gpa, choice){

    let result = await getResultsForGPA(gpa, choice);

    const roundedResult = Math.round(result * 100) / 100;
    console.log("GPA: ", roundedResult);

    let totalGradeContainer = document.querySelector(".result");
    totalGradeContainer.textContent = roundedResult;

}

function getResultsForGPA(gpa, choice = 1) {

    const roundedGPA = Math.round(gpa * 100) / 100;

    return new Promise( async (resolve, reject) => {
        let url = `http://127.0.0.1:5000/predictgpa/?gpa=${roundedGPA}&&choice=${choice}`

        let result = await fetch(url, { 
            method: 'GET'
        });

        let JSONResult = await result.json();

        let grade = JSONResult.gpa;

        resolve(grade)
    })
}
