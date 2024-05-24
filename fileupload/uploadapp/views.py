import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm


def upload_file(request):
    summary_report = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            summary_report = handle_uploaded_file(file)
    else:
        form = UploadFileForm()
    return render(request, 'uploadapp/upload.html', {'form': form, 'summary_report': summary_report})

def handle_uploaded_file(file):
    df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)

    summary_report = {
        'total_entries': len(df),
        'unique_customer_states': df['Cust State'].nunique(),
        'average_dpd': df['DPD'].mean(),
        'min_dpd': df['DPD'].min(),
        'max_dpd': df['DPD'].max(),
        'median_dpd': df['DPD'].median(),
        'std_dpd': df['DPD'].std(),
        'state_counts': df['Cust State'].value_counts().to_dict()
    }
    return summary_report
