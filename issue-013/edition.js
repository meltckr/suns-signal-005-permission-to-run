const progress=document.querySelector('.reading-progress span');
function updateProgress(){const max=document.documentElement.scrollHeight-innerHeight;progress.style.width=max>0?`${Math.min(100,scrollY/max*100)}%`:'0%';}
addEventListener('scroll',updateProgress,{passive:true});addEventListener('resize',updateProgress);addEventListener('hashchange',()=>requestAnimationFrame(updateProgress));updateProgress();
addEventListener('beforeprint',()=>document.querySelectorAll('details').forEach(el=>{el.dataset.wasOpen=String(el.open);el.open=true;}));
addEventListener('afterprint',()=>document.querySelectorAll('details').forEach(el=>{el.open=el.dataset.wasOpen==='true';}));
