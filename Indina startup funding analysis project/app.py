import pandas as pd
import numpy as np
import streamlit as st 
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title='Startup Analysis')
df = pd.read_csv('C:/Users/Lenovo/Desktop/Python/Project1/cleaned_data.csv')
df['date'] = pd.to_datetime(df['date'])
temp_inves = df['investors'].str.strip().str.title().str.split(',').sum()
temp_inves = sorted(set(temp_inves))
for i in range(len(temp_inves)):
    temp_inves[i] = temp_inves[i].strip()


# overall analysis

def overall_load():

    df['year'] = df['date'].dt.year
    st.title('📊 Startup Investment Analysis - India')
    st.markdown('---')

    # --- Top Metrics Row ---
    total_investment = round(df['amount(Cr)'].sum())
    highest_funding_startup = round(
        df.groupby('startup')['amount(Cr)'].sum().sort_values(ascending=False).head(1).values[0]

    )
    avg_investment = round(df.groupby('startup')['amount(Cr)'].sum().mean())
    col1, col2, col3 = st.columns(3)
    col1.metric(label='Total Investment', value=f'₹{total_investment} Cr')
    col2.metric(label='Highest Funded Startup', value=f'₹{highest_funding_startup} Cr')
    col3.metric(label='Average Investment', value=f'₹{avg_investment} Cr')

    st.markdown('---')
    # --- Year on Year Graph ---
    st.subheader('📈 Year on Year Trend')

    df_1 = df.groupby('year')['startup'].nunique()
    df_2 = df.groupby('year')['amount(Cr)'].sum()

    sl = st.selectbox(
        label=':rainbow[Choose Metric]',
        options=['Number of startups', 'Investment in startups']
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    if sl == 'Number of startups':

        ax.plot(df_1.index, df_1.values, marker='o', color='#00C0F2', linewidth=2)
        ax.set_ylabel('Number of Startups')
        ax.set_title('Number of Startups Funded per Year')

    elif sl == 'Investment in startups':
        ax.plot(df_2.index, df_2.values, marker='o', color='#FF4B4B', linewidth=2)
        ax.set_ylabel('Investment (Cr)')
        ax.set_title('Total Investment per Year')
    ax.set_xlabel('Year')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)

    # TOP 10 SECTORS BASED ON INVESTMENTS
    st.header("•Top 10 Sectors Driving National Investment")
    ct = df[df['amount(Cr)'] > 0]
    ct = ct['vertical'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = plt.get_cmap("cool")(np.linspace(0.85,0.15 ,10))

    ax.bar(x=ct.index, height=ct.values, color=colors)
    ax.set_ylabel("Number of Investments")
    ax.set_xlabel("Sectors")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # COL1 , COL2 FOR (TOP STARTUPS YEARLY) & (TOP INVESTERS )
    col1,col2 = st.columns(2)

    with col1:
        st.subheader(":rainbow[Year wise Top funded startups]")
        top =df.groupby(['year' ,'startup'] ,as_index=False)['amount(Cr)'].sum().sort_values(['year' ,'amount(Cr)'],
        ascending=[True,False]).drop_duplicates('year').reset_index(drop=True)
        st.dataframe(top)

    with col2:
        st.subheader(':rainbow[Top investers in Market]')
        ct = df[df['investors'] != 'Unkown']
        ct = ct.groupby('investors')['amount(Cr)'].sum().sort_values(ascending=False).head(10).reset_index()
        st.dataframe(ct)

    # CITY BASED INVESTMET GRAPH

    st.subheader("• Top 10 Cities Attracting Major Capital")
    ctemp = df.groupby('city')['amount(Cr)'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = plt.get_cmap("plasma")(np.linspace(0.15,0.85 ,10))

    ax.bar(x=ctemp.index, height=ctemp.values, color=colors)
    ax.set_ylabel("Total Investment")
    ax.set_xlabel("City")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    df['month'] = df['date'].dt.month_name()

    # HEAT MAP OF INVESTMENT
    ctemp = df.pivot_table(index='month' , columns='year' , values='amount(Cr)' , aggfunc='sum',fill_value=0)
    st.header("•Investment Heatmap by Year and Month")
    fig, ax = plt.subplots(figsize=(4, 4))

    im = ax.imshow(ctemp, cmap='viridis', aspect='equal', interpolation='nearest')

    ax.set_xticks(np.arange(6))
    ax.set_xticklabels(df['year'].sort_values().unique(), fontsize=5, rotation=45)
    ax.set_yticks(np.arange(12))
    ax.set_yticklabels(np.arange(1, 13), fontsize=5)

    # Labels and Title

    ax.set_xlabel('Year', fontsize=7, fontweight='bold', labelpad=10)
    ax.set_ylabel('Month', fontsize=7, fontweight='bold', labelpad=10)
    ax.set_title('Investment Heatmap', fontsize=7, pad=12, fontweight='bold')
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Investment', rotation=270, labelpad=15, fontsize=8)
    cbar.ax.tick_params(labelsize=6)
    fig.tight_layout()
    st.pyplot(fig)

    st.header(":rainbow[•Investment Distribution]")
    fig = px.sunburst(df,path=['city' ,'vertical' ,'startup'] ,values='amount(Cr)',
                  color_discrete_sequence=px.colors.carto.Agsunset)
    fig.update_traces(
    hovertemplate='<b>%{label}</b><br>Total investment: $%{value:.2f}<extra></extra>'
    )
    fig.update_layout(
    paper_bgcolor='white', 
    plot_bgcolor='white',   
    font=dict(color='black') 
    )
    st.plotly_chart(fig, use_container_width=True)




# investor details 
def investor_details(investor):
    st.title(investor)
    temp_df = df[df['investors'].str.contains(investor , case=False)]
    st.header(':rainbow[Last 5 investments :]')
    recent = temp_df.head()[['date' ,'city','startup','vertical','round','amount(Cr)']].reset_index(drop=True)
    st.dataframe(recent)


    # biggest investments of an investor
    biggest_investments = temp_df.groupby('startup' ,as_index=False)['amount(Cr)'].sum().sort_values(by='amount(Cr)' , ascending=False).reset_index(drop=True).head()
    st.header(':rainbow[Biggest Investments :]')
    # column wise view
    col1,col2 = st.columns(2)
    with col1:
      st.dataframe(biggest_investments)
    with col2:
       fig, ax = plt.subplots(figsize=(5, 3)) 
       colors = plt.get_cmap("plasma")(np.linspace(0.15,0.85 ,5))
       ax.bar(biggest_investments['startup'], biggest_investments['amount(Cr)'],color=colors)
       ax.set_xticklabels(biggest_investments['startup'],rotation=40)
       ax.set_ylabel("Amount(Cr)" ,fontsize=10)
       ax.set_xlabel('Startups' ,fontsize=10)
       st.pyplot(fig)

        
    # CITY BASED PIE CHART
    st.header(':rainbow[Top 5 City based Investments :]') 
    col1, col2,  = st.columns([2, 1])
    with col1:
        ct = temp_df.groupby('city')['amount(Cr)'].sum().sort_values(ascending=False)
        ct = ct[ct != 0]
        if not ct.empty and ct.sum() > 0:
          ct = ct.head(5)
          fig,ax =plt.subplots(figsize=(3,3))
          n = len(ct.values)
          colors = plt.get_cmap("cool")(np.linspace(0.15, 0.85, n))
          ax.pie(ct.values , labels=ct.index ,autopct='%1.1f%%',
                 colors=colors ,startangle=90,
                   wedgeprops={"edgecolor": "white", "linewidth": 1.5})
          ax.axis('equal') 
          st.pyplot(fig)
        else:
          st.warning('No investment data available to display ')

    st.header(':rainbow[Top 5 Sector based Investments :]') # sector pie chart 
    col1, col2,  = st.columns([2, 1])
    with col1:
          
        # investments of an investor in verticals
        verticals = temp_df.groupby('vertical')['amount(Cr)'].sum().sort_values(ascending=False).head()
        
        # Check if data exists and the total sum is greater than zero
        if not verticals.empty and verticals.sum() > 0:
            fig, ax = plt.subplots(figsize=(3, 3)) 
            n = len(verticals.values)
            colors = plt.get_cmap("viridis")(np.linspace(0.15, 0.85, n))
            ax.pie(verticals.values,colors=colors, labels=verticals.index,
                    autopct='%1.1f%%', startangle=90,
                    wedgeprops={'edgecolor':'white' , 'linewidth': 1.5})
            ax.axis('equal') 
            st.pyplot(fig)
        else:
            st.warning("No investment data available to display ")





  # Year by Year investment line graph 
    st.header(':rainbow[Year based Investment Graph :]')
    year_df = temp_df[['date', 'amount(Cr)']].copy()
    
    year_df['year'] = year_df['date'].dt.year
    year_ser = year_df.groupby('year')['amount(Cr)'].sum()

    c1, c2 = st.columns([3, 1])
    if not year_ser.empty:
        with c1:
            fig, ax = plt.subplots(figsize=(5, 3)) 
            
            ax.plot(year_ser.index, year_ser.values, marker='o', linestyle='-', color='b')
            ax.set_xlabel('Year')
            ax.set_ylabel('Total Amount (Cr)')
            
            ax.set_xticks(year_ser.index)
            ax.set_xticklabels([str(int(x)) for x in year_ser.index])
            
            ax.grid(True, linestyle='--', alpha=0.3 ,color='blue')
            st.pyplot(fig)
    else:
        st.warning("No year-wise investment data available to display.")

   # Similar investors recommendation 
    st.header(':rainbow[Similar Investors :]')
    investor_temp = temp_df
    investor_temp_startups = investor_temp['startup'].dropna().tolist()
    investor_temp_verticals = investor_temp['vertical'].dropna().tolist()
    investor_temp_subverticals = investor_temp['sub vertical'].dropna().tolist()
    investor_temp_city = investor_temp['city'].dropna().tolist()

    temp_df2 = df[df['startup'].isin(investor_temp_startups)].copy()

    
    temp_df2 = df[df['startup'].isin(investor_temp_startups)]
    if(investor_temp.shape[0] > 5):
      temp_df2 = temp_df2[temp_df2['vertical'].isin(investor_temp_verticals)]
    if(investor_temp.shape[0] > 5):
      temp_df2 = temp_df2[temp_df2['sub vertical'].isin(investor_temp_subverticals)]
    if(investor_temp.shape[0] > 5):
      temp_df2 = temp_df2[temp_df2['city'].isin(investor_temp_city)]

        
    if not temp_df2.empty:
        
        temp_df2['year'] = temp_df2['date'].dt.year
        temp_df2 = temp_df2.sort_values(['year', 'amount(Cr)'], ascending=[False, False])
        
        all_investors = temp_df2['investors'].dropna().str.split(',').explode().str.strip()
        similar_investors = all_investors[~all_investors.str.contains(investor, case=False, na=False)].unique().tolist()[:5]
        
        if similar_investors:
            for sim_inv in similar_investors:
                st.write(f"- {sim_inv}")
        else:
            st.write("No similar investors found.")
    else:
        st.write("No similar investors found.")


def show_startup_details(startup):
    st.subheader(startup)
    temp_df = df[df['startup'] == startup]
    st.header(":rainbow[Key Performance Indicators]")
    col1, col2 = st.columns(2)

    with col1:
        total_invested = np.round(temp_df['amount(Cr)'].sum(), 2)
        st.metric("Total Amount Invested", f"₹ {total_invested} Cr")

    with col2:
        highest_investment = np.round(temp_df['amount(Cr)'].max(), 2)
        st.metric("Highest Investment", f"₹ {highest_investment} Cr")

    st.divider()

    st.header(":rainbow[General Information]")
    col3, col4, col5 = st.columns(3)

    with col3:
        st.subheader("Sub Verticals")
        sub_verticals = list(temp_df['sub vertical'].dropna().unique())
        st.write(", ".join(sub_verticals))

    with col4:
        st.subheader("Locations")
        location = list(temp_df['city'].dropna().unique())
        st.write(", ".join(location))

    with col5:
        st.subheader("Investors")
        def refine(lst):
            for i in range(len(lst)):
                lst[i] = lst[i].strip()
            return lst

        investors_who_invested = set(temp_df['investors'].dropna().str.strip().str.split(',').apply(refine).sum())
        st.write(", ".join(list(investors_who_invested)))

    st.divider()

    st.header(":rainbow[Investment Analytics]")
    col1,_ = st.columns([3,1])
    with col1:
       st.subheader("Year-over-Year Investment")

       if 'year' not in temp_df.columns:
           temp_df['year'] = pd.to_datetime(temp_df['date']).dt.year

       yearly_investment = temp_df.groupby('year')['amount(Cr)'].sum()
    
       fig1, ax1 = plt.subplots(figsize=(3, 2))
       ax1.plot(yearly_investment.index, yearly_investment.values, marker='o', color='red')
       ax1.set_xlabel('Year')
       ax1.set_ylabel('Investment(Cr)')
       ax1.grid(True, linestyle='--', color='blue', alpha=0.4)
    
       st.pyplot(fig1 ,use_container_width=True)

    col2 ,_ = st.columns([3,1])
    with col2:
        st.subheader("Investment by Vertical")
        vertical_investment = temp_df.groupby('vertical')['amount(Cr)'].sum()

        if not vertical_investment.empty and vertical_investment.sum() > 0:
            fig2, ax2 = plt.subplots(figsize=(3, 3))
            n = len(vertical_investment.values)
            colors = plt.get_cmap("cool")(np.linspace(0.15, 0.85, n))
            ax2.pie(
                vertical_investment.values, 
                labels=vertical_investment.index, 
                autopct='%1.1f%%', 
                colors=colors, 
                startangle=90, 
                wedgeprops={"edgecolor": "white", "linewidth": 1.5}
            )
            st.pyplot(fig2)  
        else:
            st.warning("No investment data available to display")

    if(temp_df.shape[0] > 4):
        st.header("• Verical Based total investment")
        fig = px.pie(temp_df,names='vertical' ,values='amount(Cr)',hole=0.2 ,width=600 ,height=450,
          color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig ,use_container_width=True)


st.sidebar.title(':rainbow[Startup Funding Analysis]')
option = st.sidebar.selectbox(':rainbow[Select One]' , options=['Overall Analysis' , 'Startups' , 'Investors'])

if option == 'Overall Analysis':
    btn1 = st.sidebar.checkbox('Show  Details')
    st.title(':rainbow[Overall Analysis]')
    if btn1:
      overall_load()
elif option ==  'Startups':
    st.title('Startups Analysis')
    startup = st.sidebar.selectbox(':rainbow[Select Startup]' , options=sorted([s for s in df['startup'].dropna().unique() if str(s).title() not in temp_inves]))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        show_startup_details(startup)
elif option == 'Investors':

    investor = st.sidebar.selectbox(':rainbow[Select Investor]' , options=temp_inves)
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        investor_details(investor)
    else:
            st.title('Investors Analysis')