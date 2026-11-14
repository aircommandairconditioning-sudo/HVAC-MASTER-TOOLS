import streamlit as st
from CoolProp.CoolProp import PropsSI
st.set_page_config(page_title="HVAC MASTER TOOLS", page_icon="❄️")

st.title("❄️ HVAC MASTER TOOLS")
st.caption("Professional HVAC Engineering Calculators")

tool = st.selectbox("Select Calculator", ["BTU Calculator", "TR Calculator", "CFM Calculator", "Air Velocity Calculator", "Duct Size Calculator", "Superheat Calculator", "Subcooling Calculator", "Refrigerant Pressure-Temperature Calculator"])
if tool == "BTU Calculator":
    st.header("Room Cooling Estimate")

    length = st.number_input("Room Length (Feet)", min_value=1)
    width = st.number_input("Room Width (Feet)", min_value=1)

    if st.button("Calculate BTU"):
        btu = length * width * 25
        st.success(f"Estimated Cooling: {btu:,.0f} BTU/hr")
        st.info(f"Approximate Capacity: {btu / 12000:.2f} TR")

elif tool == "TR Calculator":
    st.header("BTU to TR Conversion")

    btu = st.number_input("Enter BTU/hr", min_value=1)

    if st.button("Calculate TR"):
        tr = btu / 12000
        st.success(f"Cooling Capacity: {tr:.2f} TR")
elif tool == "CFM Calculator":
    st.header("Airflow Calculator")

    length = st.number_input("Room Length (Feet)", min_value=1)
    width = st.number_input("Room Width (Feet)", min_value=1)
    height = st.number_input("Room Height (Feet)", min_value=1)
    ach = st.number_input("Air Changes per Hour (ACH)", min_value=0.1, value=6.0)

    if st.button("Calculate CFM"):
        cfm = length * width * height * ach / 60
        st.success(f"Required Airflow: {cfm:,.0f} CFM")
elif tool == "Air Velocity Calculator":
    st.header("Duct Air Velocity")

    cfm = st.number_input("Airflow (CFM)", min_value=1)
    duct = st.selectbox("Duct Type", ["Rectangular", "Round"])

    if duct == "Rectangular":
        width = st.number_input("Duct Width (Inches)", min_value=1)
        height = st.number_input("Duct Height (Inches)", min_value=1)
        area = width * height / 144

    else:
        diameter = st.number_input("Duct Diameter (Inches)", min_value=1)
        area = 3.14159 * (diameter / 12) ** 2 / 4

    if st.button("Calculate Velocity"):
        velocity = cfm / area
        st.success(f"Air Velocity: {velocity:,.0f} FPM")
        st.info(f"Duct Area: {area:.3f} sq.ft.")
elif tool == "Duct Size Calculator":
    st.header("Rectangular Duct Sizing")

    cfm = st.number_input("Required Airflow (CFM)", min_value=1)
    velocity = st.number_input("Target Velocity (FPM)", min_value=1, value=800)
    ratio = st.number_input("Width / Height Ratio", min_value=1.0, value=2.0)

    if st.button("Calculate Duct Size"):
        area = cfm / velocity
        width = (area * ratio) ** 0.5 * 12
        height = (area / ratio) ** 0.5 * 12

        st.success(f"Required Duct Area: {area:.3f} sq.ft.")
        st.info(f"Duct Width: {width:.1f} inches")
        st.info(f"Duct Height: {height:.1f} inches")
elif tool == "Superheat Calculator":
    st.header("Refrigerant Superheat")

    suction_temp = st.number_input("Suction Line Temperature (°C)", value=15.0)
    saturation_temp = st.number_input("Evaporator Saturation Temperature (°C)", value=5.0)

    if st.button("Calculate Superheat"):
        superheat = suction_temp - saturation_temp
        st.success(f"Superheat: {superheat:.1f} °C")

        st.success(f"Subcooling: {subcooling:.1f} °C")

    
elif tool == "Subcooling Calculator":
    st.header("Refrigerant Subcooling")

    saturation_temp = st.number_input("Condensing Saturation Temperature (°C)", value=45.0)
    liquid_temp = st.number_input("Liquid Line Temperature (°C)", value=38.0)

    if st.button("Calculate Subcooling"):
        subcooling = saturation_temp - liquid_temp

        st.success(f"Subcooling: {subcooling:.1f} °C")
elif tool == "Refrigerant Pressure-Temperature Calculator":
    st.header("Refrigerant Pressure-Temperature")
    refrigerant = st.selectbox(
        "Select Refrigerant",
        ["R134a", "R22", "R32", "R410A", "R404A", "R407C", "R290", "R600a"]
    )

    saturation_type = st.selectbox(
        "Saturation Reference",
        ["Dew Point (Vapor)", "Bubble Point (Liquid)"]
    )
    quality = 1 if saturation_type == "Dew Point (Vapor)" else 0
    mode = st.selectbox(
        "Select Calculation",
        ["Pressure to Temperature", "Temperature to Pressure"]
    )

    pressure_unit = st.selectbox(
        "Pressure Unit",
        ["bar gauge (bar g)", "bar absolute (bar a)"]
    )

    if mode == "Pressure to Temperature":
        pressure = st.number_input("Enter Pressure", min_value=0.0, value=9.0)

        if st.button("Calculate Temperature"):
            try:
                if pressure_unit == "bar gauge (bar g)":
                    absolute_pressure = (pressure + 1.01325) * 100000
                else:
                    absolute_pressure = pressure * 100000

                temp = PropsSI("T", "P", absolute_pressure, "Q", quality, refrigerant) - 273.15

                st.success(f"Saturation Temperature: {temp:.2f} °C")

            except Exception as e:
                st.error(f"Calculation Error: {e}")

    else:
        temperature = st.number_input("Temperature (°C)", value=5.0)

        if st.button("Calculate Pressure"):
            try:
                pressure = PropsSI("P", "T", temperature + 273.15, "Q", quality, refrigerant) / 100000

                if pressure_unit == "bar gauge (bar g)":
                    pressure = pressure - 1.01325
                    st.success(f"Saturation Pressure: {pressure:.2f} bar g")
                else:
                    st.success(f"Saturation Pressure: {pressure:.2f} bar a")

            except Exception as e:
                st.error(f"Calculation Error: {e}")
st.divider()
st.caption("HVAC MASTER TOOLS | Open Source Project")
st.caption("Room BTU estimate uses a simplified 25 BTU/sq.ft. rule, not a full cooling-load calculation.")