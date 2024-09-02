function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteAccount(id) {
  userId = $(id).data('id')
  fetch("/delete-account", {
    method: "POST",
    body: JSON.stringify({ userId: userId }),
  }).then((_res) => {
    window.location.href = "/list_account";
  });
}

function deleteExam(id) {
  examId = $(id).data('id')
  fetch("/delete-exam", {
    method: "POST",
    body: JSON.stringify({ examId: examId }),
  }).then((_res) => {
    window.location.href = "/list_exam";
  });
}

function editAccount(userId) {
  userId = $(id).data('id')
  fetch("/edit_user", {
    method: "POST",
    body: JSON.stringify({ userId: userId }),
  }).then((_res) => {
    window.location.href = "/edit_account";
  });
}

function editExam(examId) {
  examId = $(id).data('id')
  fetch("/edit_exam", {
    method: "POST",
    body: JSON.stringify({ examId: examId }),
  }).then((_res) => {
    window.location.href = "/edit_exam";
  });
}

