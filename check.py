import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learnloop.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db.models import CASCADE

User = get_user_model()
print("\n--- SCANNING DATABASE MODELS ---")

found_blocker = False
for rel in User._meta.related_objects:
    # Check if the deletion rule is NOT Cascade
    if rel.on_delete != CASCADE:
        print(f"⚠️  BLOCKER FOUND: Model '{rel.related_model.__name__}' inside app '{rel.related_model._meta.app_label}'")
        print(f"    Field Name: {rel.field.name}")
        print(f"    Current Rule: {rel.on_delete}")
        found_blocker = True

if not found_blocker:
    print("✅ No blocking models found. The issue might be in the database state itself.")
else:
    print("\nTo fix: Go to the models listed above and change on_delete to models.CASCADE")