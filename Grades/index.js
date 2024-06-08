function getResultsForNextGrade(data) {

    return new Promise( async (resolve, reject) => {
        let url = `http://127.0.0.1:5000/predict/?data=${data}`

        let result = await fetch(url, { 
            method: 'GET'
        });

        let JSONResult = await result.json();

        let grade = JSONResult.grade;
        resolve(grade)
    })
}

async function predictNextGrade(){

    let inputContainer = document.querySelector(".input-container");
    let inputs = inputContainer.querySelectorAll("input");

    let grades = {
        "G1": inputs[0].value,
        "G2": inputs[1].value
    }

    var jsonString = encodeURIComponent(JSON.stringify(grades));

    let areZeros = grades["G1"] == 0 && grades["G2"] == 0;
    let result = areZeros ? 0 : await getResultsForNextGrade(jsonString);

    let totalGradeContainer = document.querySelector("#totalGradeScore");
    totalGradeContainer.textContent = result;

}