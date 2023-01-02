let today=new Date()
let tomorrow=new Date(today.setDate(today.getDate() + 1)).toLocaleDateString('en-ca')
document.querySelector("#date").min=tomorrow 
const timechoose=document.querySelector("#timechoose")
radiomorning=document.querySelector("input[name='time']")
timechoose.addEventListener("change", function tapradio(){
    let morningchecked=radiomorning.checked
    if(!morningchecked){
       document.getElementById("price2000").hidden=true
       document.getElementById("price2500").hidden=false
    }
    else{
        document.getElementById("price2000").hidden=false
        document.getElementById("price2500").hidden=true

    }})
const bookingButton=document.querySelector(".bookingButton")
const date=document.querySelector("#date")
if (!date.value){
        bookingButton.disabled=true  
    }
date.addEventListener("change",function(e){
    if (date.value){
        bookingButton.disabled=false  
    }else {
        bookingButton.disabled=true  
    }
})
bookingButton.addEventListener("click", function(e){
    if(document.cookie){
        let price=document.querySelector(".cost:not([hidden])");
        price=parseInt((price.id).replace("price", ""))
        const attractionId=parseInt((location.pathname).replace("/attraction/", ""))
        let data={
            "attractionId": attractionId,
            "date": date.value,
            "time": document.querySelector("input[name='time']:checked").id,
            "price": price,
            "memberId":id
        }
        fetch("/api/booking", {
            method:"POST",
            headers:{"Content-Type": "application/json"},
            body:JSON.stringify(data)
        }).then(function(response){return response.json();})
        .then(function(data){
            if(data.ok){
                location.href="/booking"
            }
        })
    }else{
        signIn.style.display="flex"
        mask.style.display="block"
    }
})

url="http://3.114.72.60:3000/api"+location.pathname
fetch(url).then(function(response){return response.json();
}).then(function(data){
    const description = document.querySelector(".description")
    description.textContent = data.data.description

    const address = document.querySelector(".address")
    address.textContent = data.data.address

    const transport = document.querySelector(".transport")
    transport.textContent = data.data.transport

    const name = document.querySelector(".name")
    name.textContent = data.data.name
    document.querySelector("title").textContent=data.data.name+"-台北一日遊"

    const mrtcategory = document.querySelector(".mrtcategory")
    mrtcategory.textContent = data.data.category+" at "+data.data.mrt

    const imgcontainer = document.querySelector(".imgcontainer")
    const dotcontainer = document.querySelector(".dotcontainer")
    const images = data.data.image
    for(let i = 0; i < images.length; i++) {
        let img = document.createElement("img");
        img.className = "img";
        img.src = data.data.image[i];
        imgcontainer.appendChild(img);
        let dot = document.createElement("span");
        dot.id = "dot";
        dotcontainer.appendChild(dot);
    }

    let slideIndex = 1;
    showSlides(slideIndex);

    const prev = document.querySelector(".prev")
    const next = document.querySelector(".next")
    prev.addEventListener( "click", function(){plusSlides(-1)} )
    next.addEventListener( "click", function(){plusSlides(1)} )
    function plusSlides(n) {
        showSlides(slideIndex += n);
    }

    function showSlides(n) {
        let slides = document.getElementsByClassName("img");
        let dots = document.querySelectorAll("#dot");
        if (n > slides.length) { slideIndex = 1 }
        if (n < 1) { slideIndex = slides.length }
        for (let i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
            dots[i].className = "dot";
        }
        slides[slideIndex - 1].style.display = "block";
        dots[slideIndex - 1].className = "activedot";
    }
    loaded(imgloaded)
})
let i=0
const imgloaded=function (){
    const images=document.querySelectorAll(".img")
    images.forEach(image =>{
        const img=new Image()
        img.src=image.src
        img.addEventListener("load",()=>{
            i+=1
            if(images.length === i){
                document.querySelector("#imgloaded").style.display="flex"
                document.querySelector("#imgloading").style.display="none"
            }
        })
    })
}
