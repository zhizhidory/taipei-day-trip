fetch("/api/user/auth",{
    method:"GET",
    credentials: "include",
    headers:{"Content-Type": "application/json"}
}).then(function(response){return response.json()}).then(function(result){
    if (!result.data) {
         return location.href="/"
    } 
    return shownumber()               
})
function shownumber(){
    const number=(location.search).replace("?number=", "")
    document.querySelector(".ordernumber>span").textContent=number
    return loaded()
}
document.querySelector("footer").className="footer_thankyou"
