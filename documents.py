class Document:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author
        self.reviews = []
        self.approved = False
    def review(self, role, review):
        if role.permissions.can_review:
            self.reviews.append((role, review))
        else:
            raise PermissionError(f"{role.name} does not have permission to review documents")
    def approve(self, role, approval):
        if role.permissions.can_approve:
            self.approved = True
            self.approval = approval
        else:
            raise PermissionError(f"{role.name} does not have permission to approve documents")
        
    def edit(self, role, edit):
        if role.permissions.can_edit:
            self.content = edit
        else:
            raise PermissionError(f"{role.name} does not have permission to edit documents")