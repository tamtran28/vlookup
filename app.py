import streamlit as st
import pandas as pd

st.title("🔍 Công cụ so sánh 2 file – VLOOKUP theo STT")

file1 = st.file_uploader("📄 File 1 (file chính cần cập nhật)", type=["xlsx"])
file2 = st.file_uploader("📄 File 2 (file chứa dữ liệu cần lấy)", type=["xlsx"])

if file1 and file2:
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Chuẩn hóa tên cột
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # Tên cột theo yêu cầu
    cols_needed = [
        "TÌNH HÌNH KPCS",
        "NGÀY HOÀN TẤT KPCS (mm/dd/yyyy)",
        "TRÌNH TRANG KPCS (Đã KP, Đang KP; Chưa KP)"
    ]

    # Kiểm tra cột trong file 2
    missing = [c for c in cols_needed if c not in df2.columns]
    if missing:
        st.error(f"❌ File 2 thiếu các cột: {missing}")
    else:
        # VLOOKUP dựa trên STT
        result = df1.merge(
            df2[["STT"] + cols_needed],
            on="STT",
            how="left"
        )

        # Chuyển định dạng ngày mm/dd/yyyy
        date_col = "NGÀY HOÀN TẤT KPCS (mm/dd/yyyy)"
        if date_col in result.columns:
            result[date_col] = pd.to_datetime(
                result[date_col], errors="coerce"
            ).dt.strftime("%m/%d/%Y")

        # Fix lỗi JSON của Streamlit
        safe_result = result.fillna("").astype(str)

        st.subheader("📌 Kết quả sau khi đối chiếu")
        st.dataframe(safe_result)

        # Xuất file Excel
        output = "ket_qua_kpcs.xlsx"
        result.to_excel(output, index=False)

        with open(output, "rb") as f:
            st.download_button(
                label="⬇️ Tải file kết quả",
                data=f,
                file_name=output,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
