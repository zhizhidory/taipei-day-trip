const signout=document.querySelector("#signout")
signout.style.display="none"
const signUpIn=document.querySelector("#signUpIn")
let id
// 檢查登入狀態
fetch("/api/user/auth",{
    method:"GET",
    credentials: "include",
    headers:{"Content-Type": "application/json"}
}).then(function(response){return response.json()}).then(function(result){
    if (result.data){
        ({id}=result.data)
        signout.style.display="block"
        signUpIn.style.display="none"
    }
})
// 點擊登出按鈕
signout.addEventListener("click",function(e){
    fetch("/api/user/auth",{method:"DELETE"}).then(function(response){
        return response.json();}).then(function(data){
        location.reload();
    })
})
// 點擊註冊按鈕
const signUpButton=document.querySelector("#signUpButton")
const signUpResponse=document.querySelector("#signUp>.dataResponse")
signUpButton.addEventListener("click",function(e){
    let data={}
    signUpResponse.style.display="none"
    SignUpInput=document.querySelectorAll("#signUp>input")
    const regex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/
    const inputEmail=SignUpInput[1].value
    for (let i=0; i<SignUpInput.length; i++){
        let inputdata=SignUpInput[i].value
        if (!inputdata){
            data=null;
            break;
        }
        data[SignUpInput[i].id]=SignUpInput[i].value
    }
    // 驗證輸入註冊資料格式不能空白和email格式
    if(!data || !regex.test(inputEmail)){
        signUpResponse.textContent="輸入資料格式有錯";
        signUpResponse.style.display="block";
        return
    }
    // 將註冊資料送到後端
    fetch("/api/user",{method:"POST", headers:{"Content-Type": "application/json"},
    body:JSON.stringify(data)}).then(function(response){return response.json();
    }).then(function(data){
        if(data.error){
            signUpResponse.style.display="block"
            signUpResponse.textContent=data.message
            return
        }
        signUpResponse.style.display="block"
        signUpResponse.style.color="black"
        signUpResponse.textContent="註冊成功!請重新登入"
    })
})
// 點擊登入按鈕
const signInButton=document.querySelector("#signInButton")
const signInResponse=document.querySelector("#signIn>.dataResponse")
signInButton.addEventListener("click", function(){
    signInResponse.style.display="none"
    const signInData=document.querySelectorAll("#signIn>input")
    let data={email:signInData[0].value, password:signInData[1].value}
    fetch("/api/user/auth", {method:"PUT", headers:{"Content-Type": "application/json"},
    body:JSON.stringify(data)}).then(function(response){
        return response.json()
    }).then(function(result){
        if (result.error){
            signInResponse.style.display="block"
            signInResponse.textContent="帳號或密碼輸入錯誤"
            return
        }
        location.reload()
    })
})

const mask=document.querySelector(".mask")
const signIn=document.querySelector("#signIn")
const signUp=document.querySelector("#signUp")
// 回首頁
const BacktoHome=document.querySelector(".leftnav")
BacktoHome.addEventListener("click",function(){
    location.href="/"
})

const toSignUp=document.querySelector("#toSignUp")
toSignUp.addEventListener("click",function(){
    signIn.style.display="none"
    signUp.style.display="flex"
    signUpResponse.style.display="none"
})
const toSignIn=document.querySelector("#toSignIn")
toSignIn.addEventListener("click",function(){
    signIn.style.display="flex"
    signUp.style.display="none"
    signInResponse.style.display="none"

})

const signpages=document.querySelectorAll(".sign")
signpages.forEach( closepage => {closepage.addEventListener("click", function(e){
    if (e.target.className == "x"){
        this.style.display="none"
        mask.style.display="none"
}})});
signUpIn.addEventListener("click", function(){
    signIn.style.display="flex"
    mask.style.display="block"
})
