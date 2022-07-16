mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
[theme]\n\
primaryColor = '#26A18D'\n\
backgroundColor = '#FFFFFF'\n\
secondaryBackgroundColor = '#F3F3F3'\n\
textColor = '#023047'\n\
font = 'sans serif'\n\
\n\
" > ~/.streamlit/config.toml
