const menuButton=document.querySelector('.menu-toggle');
const nav=document.querySelector('.nav');
menuButton.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';menuButton.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});
nav.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{menuButton.setAttribute('aria-expanded','false');nav.classList.remove('open')}));

document.querySelectorAll('.filter').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('.filter').forEach(filter=>{filter.classList.remove('active');filter.setAttribute('aria-selected','false')});
  button.classList.add('active');button.setAttribute('aria-selected','true');
  const category=button.dataset.filter;
  document.querySelectorAll('.product-card').forEach((card,index)=>{
    const visible=category==='tous'||card.dataset.category.split(' ').includes(category);
    card.classList.toggle('hidden',!visible);
    if(visible){card.style.animation='none';void card.offsetWidth;card.style.animation=`rise .38s ${index*.04}s both`}
  });
}));

const modal=document.querySelector('.order-modal');
const orderList=document.querySelector('.order-list');
const emptyNote=document.querySelector('.empty-note');
const selection=new Map();
function renderOrder(){orderList.innerHTML='';selection.forEach((count,name)=>{const item=document.createElement('li');const label=document.createElement('span');label.textContent=`${name} · ${count}`;const remove=document.createElement('button');remove.className='remove-item';remove.textContent='Retirer';remove.setAttribute('aria-label',`Retirer ${name}`);remove.addEventListener('click',()=>{selection.delete(name);renderOrder()});item.append(label,remove);orderList.append(item)});emptyNote.hidden=selection.size>0}
function openModal(){modal.classList.add('open');modal.setAttribute('aria-hidden','false');document.body.classList.add('modal-open');renderOrder();document.querySelector('.modal-close').focus()}
function closeModal(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true');document.body.classList.remove('modal-open')}
document.querySelectorAll('.plus').forEach(button=>button.addEventListener('click',()=>{const name=button.closest('.product-card').querySelector('h3').textContent;selection.set(name,(selection.get(name)||0)+1);openModal()}));
document.querySelectorAll('.open-order').forEach(button=>button.addEventListener('click',openModal));
document.querySelector('.modal-close').addEventListener('click',closeModal);
document.querySelector('.modal-backdrop').addEventListener('click',closeModal);
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&modal.classList.contains('open'))closeModal()});

const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('in-view');observer.unobserve(entry.target)}}),{threshold:.1});
document.querySelectorAll('.values article,.review-card,.visit-copy,.product-card').forEach(el=>observer.observe(el));

document.querySelectorAll('.gallery-filter').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('.gallery-filter').forEach(filter=>{filter.classList.remove('active');filter.setAttribute('aria-pressed','false')});
  button.classList.add('active');button.setAttribute('aria-pressed','true');
  const category=button.dataset.galleryFilter;
  document.querySelectorAll('.gallery-card').forEach((card,index)=>{
    const visible=category==='tous'||card.dataset.galleryCategory===category;
    card.hidden=!visible;
    if(visible){card.style.animation='none';void card.offsetWidth;card.style.animation=`rise .38s ${Math.min(index,8)*.035}s both`}
  });
}));