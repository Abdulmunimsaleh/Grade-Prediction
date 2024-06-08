async function predictGPA(grades, choice){

    var jsonString = encodeURIComponent(JSON.stringify(grades));

    let result = await getResultsForGPA(jsonString, choice);

    const roundedResult = Math.round(result * 100) / 100;
    console.log("GPA: ", roundedResult);

    let totalGradeContainer = document.querySelector(".result");
    totalGradeContainer.textContent = roundedResult;

}

function getResultsForGPA(data, choice = 1) {

    return new Promise( async (resolve, reject) => {
        let url = `http://127.0.0.1:5000/predict/?data=${data}&&choice=${choice}`

        let result = await fetch(url, { 
            method: 'GET'
        });

        let JSONResult = await result.json();

        let grade = JSONResult.gpa;

        resolve(grade)
    })
}
