let num = [5, 8, 2, 9, 3]

console.log(num)
num[5] = 6
console.log(num)
num.sort()
num.push(7)

// console.log(num)
// console.log(`${num.length}`)
// console.log(`${num[1]}`)
// for(let pos = 0;pos<num.length;pos++){
//     console.log(num[pos])
// }
for(let pos in num){
    console.log(num[pos])
}
console.log(num.indexOf(7))
console.log(num.indexOf(1))