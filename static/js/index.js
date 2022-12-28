let isLoading=false
const input=document.querySelector("input")
const searchbar=document.querySelector(".searchbar")
const body=document.querySelector("body")
const container=document.querySelector(".container");
fetch("http://3.114.72.60:3000/api/categories").then(function(response){
        return response.json();
}).then(function(data){
    const categories=data.data
    searchbar.addEventListener("click",tapCategory)
    for(let n=0;n<categories.length;n++){
        let category=document.createElement("div")
        category.className="category"
        category.textContent=categories[n]
        searchbar.appendChild(category)
    }
    return loaded()
})
function tapCategory(e){
    input.value=e.target.textContent
}

input.addEventListener("click",tapInput)
function tapInput(e){
    e.stopPropagation()
    searchbar.style.display="grid"
}

body.addEventListener("click",tapanyway)
function tapanyway(e){
    searchbar.style.display="none"
}

let page=0
search = function (){
    let keyword=document.querySelector("#keyword").value;
    observer.unobserve(loadingObserver)
    container.innerHTML="";
    let data=[]
    page=0
    fetch("http://3.114.72.60:3000/api/attractions?page="+page+"&keyword="+keyword).then(function(response){
        return response.json();
    }).then(function(totaldata){
    data=totaldata.data
      if (data && data.length){
        page=0 
        observer.observe(loadingObserver);            
    }else{
        let nodata=document.createElement("div")
        nodata.textContent="沒有符合結果，請重新查詢"
        nodata.className="nodata"
        container.appendChild(nodata)
    }})}
const loadingObserver = document.querySelector('footer');
const fetchdata=function (){
let keyword=document.querySelector("#keyword").value;
fetch("http://3.114.72.60:3000/api/attractions?page="+page+"&keyword="+keyword).then(function(response){
        return response.json();
}).then(function(totaldata){
    let data=totaldata.data
    for (let i=0; i<data.length ;i++){
        http=data[i].image
        let box=document.createElement("a")
        let name = document.createElement('div');
        let nametext = document.createElement('div');
        box.className="box";
        box.href="/attraction/"+parseInt(data[i].id)                   
        box.id="photo"+((page)*12+i);
        container.appendChild(box);
        let boxid=document.querySelector("#photo"+((page)*12+i));
        let img = document.createElement('img');
        img.src=http[0];
        boxid.appendChild(img);
        nametext.textContent=data[i].name
        name.className="name";
        nametext.className="nametext"
        boxid.appendChild(name)
        name.appendChild(nametext)

        let titlei = document.createElement('div');
        titlei.className="title";
        titlei.id="title"+((page)*12+i);
        boxid.appendChild(titlei);

        let titletext=document.querySelector("#title"+((page)*12+i))
        let text=document.createElement("div")
        let text2=document.createElement("div")
        text.className="titletext"
        text2.className="titletext"
        text.textContent=data[i].mrt;
        text2.textContent=data[i].category;
        titletext.appendChild(text);
        titletext.appendChild(text2);
    }
        isLoading=false  
        page=totaldata.nextPage;  
}
)};

const options = {
rootMargin: '0px 0px 400px 0px',
threshold: 0.5
}

const callback = ([entry]) => {
if (entry && entry.isIntersecting && page!=null && !isLoading ) {
    isLoading=true
    fetchdata()
}}

let observer = new IntersectionObserver(callback, options)
observer.observe(loadingObserver);
