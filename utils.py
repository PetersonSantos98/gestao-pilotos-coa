from datetime import datetime, date

def formatar_data(data_str):
    if not data_str:
        return "N/A", ""

    try:
        dt = datetime.strptime(data_str, "%Y-%m-%d").date()
        status = "val-expirada" if dt < date.today() else "val-ok"
        return dt.strftime("%d/%m/%Y"), status
    except:
        return "Inválida", ""
