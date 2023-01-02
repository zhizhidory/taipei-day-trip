const script=document.querySelector("#script")
const phoneregex = /^09+\d{8}$/
const emailregex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/
const inputemail=document.querySelector("input[type='email']")
let order, id
fetch("/api/user/auth",{credentials: "include"}
).then(response => response.json()).then(function(result){
    if(result.data){
        ({name, email, id}=result.data)
        document.querySelectorAll("#username").forEach(function(element, index){
            if(index===0){element.textContent=name;}
            else{element.value=name;}
        })
        inputemail.value=email;
    } else{
        location.href="/"
    }
    return fetch("/api/booking",{ credentials: "include",headers:{"Content-Type": "application/json"}})
}).then(response => response.json()).then(function(result){
    order=result.data
     if (result.data){
        script.src="https://js.tappaysdk.com/sdk/tpdirect/v5.14.0"
        let {date, time, price, attraction}=result.data;
        let{name, address, image}=attraction;
        if (time==="morning"){
            time = "早上9點到下午4點";
        } else {
            time = "下午兩點到晚上7點";
        };
        price = "新台幣"+price+"元"
        let data=[name, date, time, price, address]
        document.querySelector(".image>img").src=image
        emptyspans=document.querySelectorAll(".bookingtext span")
        emptyspans.forEach(function (span, index) {span.textContent=data[index]
        });
        document.querySelector(".total_price>span").textContent=price
        document.querySelectorAll("article").forEach(element => { element.style.display="flex" });
        document.querySelector(".nodata").style.display="none"
        document.querySelector("footer").className=""
    }else{
        loaded()
    }
})
document.querySelectorAll("article").forEach(element => { element.style.display="none" });
document.querySelector(".nodata").textContent="目前無任何待預定行程"
document.querySelector("footer").className="footer_nodata"
const phone=document.querySelector("#phone")
const submitButton=document.querySelector(".submitButton")
const inputname=document.querySelector("input")

document.querySelector("article>img").addEventListener("click",function(){
    fetch("api/booking",{
        method:"DELETE",
        headers:{"Content-Type": "application/json"},
        body:JSON.stringify({memberId:id})
    }).then(function(response){return response.json();}).then(function(response){
        if(response.ok){
            location.reload()
        }
    })
})
script.onload=function(){
    TPDirect.setupSDK(126896,'app_T1p0CM8fV7bUhCSYXuQQCpECIAi6oGEYJahmZ8Je4knkNCZExz64Fh9IeIVU', 'sandbox')
    TPDirect.card.setup({
        fields :{
            number: {
                element: '#card-number',
                placeholder: '**** ***** **** ****'
            },
            expirationDate: {
                element: '#card-expiration-date',
                placeholder: 'MM / YY'
            },
            ccv: {
                element: '#card-ccv',
                placeholder: 'CCV'
            }
        },
        styles: {
            'input': {
                'color': 'gray'
            },
            ':focus': {
                'color': 'gray'
            },
            '.valid': {
                'color': 'green'
            },
            '.invalid': {
                'color': 'orange'
            },
        }
    })
    TPDirect.card.onUpdate(function (update) {
        if (update.canGetPrime &&  phoneregex.test(phone.value) && emailregex.test(inputemail.value) && inputname.value) {
            submitButton.removeAttribute('disabled')
        } else {
            submitButton.setAttribute('disabled', true)
        }
    })
    const iframe=document.querySelector("iframe")
    iframe.onload=function(){
        document.getElementById("loading").style.display = "none";
        document.getElementById("loaded").style.display = "block";
    }
}
phone.addEventListener("keyup",function(){
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()
    if (tappayStatus.canGetPrime === true && phoneregex.test(phone.value) && emailregex.test(inputemail.value) && inputname.value) {
        submitButton.removeAttribute('disabled')
    } else{
        submitButton.setAttribute('disabled', true)
    }
    if (phoneregex.test(phone.value)){
        phone.style.color="green"
    }else{
        phone.style.color="orange"
    }
})
inputemail.addEventListener("keyup",function(){
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()
    if (tappayStatus.canGetPrime === true && phoneregex.test(phone.value) && emailregex.test(inputemail.value) && inputname.value) {
        submitButton.removeAttribute('disabled')
    } else{
        submitButton.setAttribute('disabled', true)
    }
    if (emailregex.test(inputemail.value)){
        inputemail.style.color="green"
    }else{
        inputemail.style.color="orange"
    }
})
inputname.addEventListener("keyup",function(){
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()
    if (tappayStatus.canGetPrime === true && phoneregex.test(phone.value) && emailregex.test(inputemail.value) && inputname.value) {
        submitButton.removeAttribute('disabled')
    } else{
        submitButton.setAttribute('disabled', true)
    }
})
submitButton.addEventListener("click", onSubmit)
function onSubmit(event) {
    event.preventDefault()
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            console.log(result.msg)
            return
        }
        let cardholderinfo=document.querySelectorAll("label>input")
        let [name, email, phone_number]=cardholderinfo
        let{price, ...trip}=order
        order = { "price":price, trip,                       
                "contact": { "name": name.value, "email": email.value, "phone": phone_number.value}
                }
        url="/api/orders"
        let data={ "prime": result.card.prime, order}
        fetch(url,{
            method:"POST",
            credentials: "include",
            headers:{"Content-Type": "application/json", },
            body:JSON.stringify(data)
        }).then(response =>response.json()).then(function(result){
            if (result.data){
                location.href="/thankyou?number="+result.data.number
            }else{
                console.log(result)
            }
        })
    })
}
