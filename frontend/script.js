document.getElementById('nuke-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = new FormData(e.target);
  const data = Object.fromEntries(form.entries());
  data.regions = form.getAll('regions');

  const status = document.getElementById('status');
  status.innerText = '🚀 AWS 리소스 탐색 중...';

  const response = await fetch('/generate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data),
  });

  const result = await response.json();

  if (response.ok) {
    status.innerText = '✅ AWS 리소스 삭제 중...';
  } else {
    status.innerText = `❌ 실패: ${result.error}`;
  }
});
