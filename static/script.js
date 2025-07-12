document.getElementById("nukeForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  const selectedRegions = [];
  form.querySelectorAll('input[name="regions"]:checked').forEach((el) => {
    selectedRegions.push(el.value);
  });

  const data = {
    alias: formData.get("alias"),
    iam_user: formData.get("iam_user"),
    iam_profile: formData.get("iam_profile"),
    account_id: formData.get("account_id"),
    exclude_id: formData.get("exclude_id") || "",
    regions: selectedRegions,
    aws_access_key: formData.get("aws_access_key"),
    aws_secret_key: formData.get("aws_secret_key")
  };

  document.getElementById("status").innerText = "🟡 AWS 리소스 탐색 중...";

  try {
    const response = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (result.success) {
      document.getElementById("status").innerText = "✅ 성공적으로 삭제되었습니다.";
    } else {
      document.getElementById("status").innerText = `❌ 실패: ${result.message}`;
    }
  } catch (error) {
    document.getElementById("status").innerText = "❌ 오류 발생: " + error.message;
  }
});
