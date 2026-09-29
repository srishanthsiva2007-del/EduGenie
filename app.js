const task = document.getElementById('task');
const input = document.getElementById('inputText');
const result = document.getElementById('result');
const submit = document.getElementById('submitBtn');
const status = document.getElementById('status');

task.addEventListener('change', () => {
  const placeholders = {
    qa: 'Example: What is the difference between AI and Machine Learning?',
    explain: 'Example: Explain object-oriented programming',
    quiz: 'Paste a lesson, chapter, or topic content here...',
    summarize: 'Paste the educational content you want to summarize...',
    learn: 'Example: Learn Python programming from beginner to advanced'
  };
  input.placeholder = placeholders[task.value];
});

function renderQuiz(items){
  result.classList.remove('empty');
  result.innerHTML = items.map((q,i)=>`<div class="quiz-item"><h4>${i+1}. ${escapeHtml(q.question)}</h4><ol type="A">${q.options.map(o=>`<li>${escapeHtml(o)}</li>`).join('')}</ol><div class="answer">Answer: ${escapeHtml(q.correct_answer)}</div><div>${escapeHtml(q.explanation)}</div></div>`).join('');
}
function escapeHtml(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML;}

submit.addEventListener('click', async () => {
  const text = input.value.trim();
  if(!text){result.className='result error';result.textContent='Please enter a question or educational content.';return;}
  submit.disabled=true; submit.textContent='Generating...'; status.textContent='Working';
  const routes={qa:'/qa',explain:'/explain',quiz:'/quiz',summarize:'/summarize',learn:'/learn/recommendations'};
  const key=task.value;
  const body=(key==='quiz'||key==='summarize')?{text}:{question:text};
  try{
    const res=await fetch(routes[key],{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    const data=await res.json();
    if(!res.ok) throw new Error(data.detail||'Request failed');
    if(key==='quiz') renderQuiz(data.quiz); else {result.className='result';result.textContent=data.result;}
    status.textContent='Ready';
  }catch(err){result.className='result error';result.textContent=err.message;status.textContent='Error';}
  finally{submit.disabled=false;submit.textContent='Generate';}
});

document.getElementById('clearBtn').addEventListener('click',()=>{input.value='';result.className='result empty';result.textContent='Your AI-generated result will appear here.';});
document.getElementById('copyBtn').addEventListener('click',async()=>{await navigator.clipboard.writeText(result.innerText);status.textContent='Copied';setTimeout(()=>status.textContent='Ready',1200);});
