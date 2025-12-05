import streamlit as st
import pandas as pd

st.set_page_config(page_title="VLOOKUP KPCS", layout="wide")
st.title("🔍 Công cụ đối chiếu 2 file – VLOOKUP theo STT")

# --- Upload files ---
file1 = st.file_uploader("📄 File 1 (danh sách cần cập nhật)", type=["xlsx"])
file2 = st.file_uploader("📄 File 2 (file chứa dữ liệu cần lấy)", type=["xlsx"])

if file1 and file2:

    # Đọc Excel
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Chuẩn hóa tên cột
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # Các cột cần lấy từ File 2
    cols_needed = [
        "TÌNH HÌNH KPCS",
        "NGÀY HOÀN TẤT KPCS (mm/dd/yyyy)",
        "TRÌNH TRANG KPCS (Đã KP, Đang KP; Chưa KP)"
    ]

    # Kiểm tra thiếu cột
    missing = [c for c in cols_needed if c not in df2.columns]
    if missing:
        st.error(f"❌ File 2 thiếu các cột sau: {missing}")
        st.stop()

    # Merge như VLOOKUP
    merged = df1.merge(
        df2[["STT"] + cols_needed],
        on="STT",
        how="left"
    )

    # Format ngày mm/dd/yyyy
    date_col = "NGÀY HOÀN TẤT KPCS (mm/dd/yyyy)"
    if date_col in merged.columns:
        merged[date_col] = pd.to_datetime(
            merged[date_col], errors="coerce"
        ).dt.strftime("%m/%d/%Y")

    # FIX lỗi Arrow / JSON khi Streamlit hiển thị
    safe_result = merged.fillna("").astype(str)

    st.subheader("📌 Kết quả sau khi đối chiếu")
    
    # Dùng data_editor thay dataframe để tránh ArrowTypeError
    st.data_editor(safe_result, use_container_width=True)

    # Xuất file Excel
    output = "ket_qua_kpcs.xlsx"
    merged.to_excel(output, index=False)

    with open(output, "rb") as f:
        st.download_button(
            label="⬇️ Tải file kết quả",
            data=f,
            file_name=output,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
