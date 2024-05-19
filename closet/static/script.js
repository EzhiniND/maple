document.addEventListener('DOMContentLoaded',()=>{
    const sidenav=document.querySelector('.sidenav');
    const btnNav=document.querySelector('#btnnav');
    const ovderlayscreen=document.querySelector('.nav-overlay');


    btnNav.addEventListener('click',()=>{
        sidenav.classList.add('open');
    })

    ovderlayscreen.addEventListener('click',()=>{
        sidenav.classList.remove('open');
    })



})