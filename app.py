import streamlit as st
import pandas as pd

st.title("🔍 Công cụ so sánh 2 file – VLOOKUP theo STT")

st.write("Tải lên 2 file Excel để đối chiếu và lấy dữ liệu như VLOOKUP")

file1 = st.file_uploader("📄 File 1 (file chính cần cập nhật)", type=["xlsx"])
file2 = st.file_uploader("📄 File 2 (file chứa dữ liệu cần lấy)", type=["xlsx"])

if file1 and file2:
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    st.success("Đã tải xong 2 file!")

    # Chuẩn hoá tên cột để tránh lỗi
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # Các cột cần lấy từ file 2
    cols_needed = [
        "TÌNH HÌNH KPCS",
        "NGÀY HOÀN TẤT KPCS (mm/dd/yyyy)",
        "TRÌNH TRANG KPCS (Đã KP, Đang KP; Chưa KP)"
    ]

    # Kiểm tra xem file 2 có đủ cột không
    missing = [c for c in cols_needed if c not in df2.columns]
    if missing:
        st.error(f"❌ File 2 thiếu các cột: {missing}")
    else:
        # Merge giống VLOOKUP: df1 ← df2 theo STT
        result = df1.merge(
            df2[["STT"] + cols_needed],
            on="STT",
            how="left"
        )

        # Format ngày mm/dd/yyyy nếu có
        if "NGÀY HOÀN TẤT KPCS (mm/dd/yyyy)" in result.columns:
            result["NGÀY HOÀN TẤT KPCS (mm/dd/yyyy)"] = pd.to_datetime(
                result["NGÀY HOÀN TẤT KPCS (mm/dd/yyyy)"], errors="coerce"
            ).dt.strftime("%m/%d/%Y")

        st.subheader("📌 Kết quả sau khi đối chiếu")
        st.dataframe(result)

        # Cho phép tải xuống
        output = "ket_qua_kpcs.xlsx"
        result.to_excel(output, index=False)

        with open(output, "rb") as f:
            st.download_button(
                label="⬇️ Tải file kết quả",
                data=f,
                file_name=output,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
