// let setA = new Set(["MTH101", "MTH201", "ECC333"])
let setB = ["MTH101", "ECC433", "PHY553"]
// // console.log(new Set([...setA, ...setB]))
// console.log(setB.difference(setA))

const index = setB.indexOf("ECC433")
setB.splice(index, 1)
console.log(setB)