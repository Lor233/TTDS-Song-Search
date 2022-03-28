import React, { Component, Fragment } from 'react'
import { Container, Skeleton, createTheme, ThemeProvider, Typography, AppBar, Toolbar, CssBaseline } from '@mui/material'
import Result from './components/Result.js'
import SearchInput from './components/SearchInput.js'
import API from './components/API.js'
import './App.css'
import queryInfo from './components/globalData';
import LyricsOutlinedIcon from '@mui/icons-material/LyricsOutlined';


const theme = createTheme({
      palette: {
        primary: {
          //main: '#2196f3',
          //main:'#F3F3F3'
          main: '#242424'
        },
        secondary: {
          main: '#ffffff',
        },
        box:{
          main: '#2196f3',
        }
      },
    })

export default class App extends Component {
  
  constructor(props) {
    super(props)
    this.state = {
      // songs: [{songName:'True Love',singer:'a1',lyrics:"Rich man, poor man, beggar or king,\n You just can't have everything.\nSo thank your stars above\nFor a song in your heart."},{songName:'a',singer:'a1',lyrics:'a2'},{songName:'a',singer:'a1',lyrics:'a2'},{songName:'a',singer:'a1',lyrics:'a2'},{songName:'a',singer:'a1',lyrics:'a2'},{songName:'a',singer:'a1',lyrics:'a2'},{songName:'a',singer:'a1',lyrics:'a2'},{songName:'a',singer:'a1',lyrics:'a2'},{songName:'a',singer:'a1',lyrics:'a2'},{songName:'a',singer:'a1',lyrics:'a2'},{songName:'a',singer:'a1',lyrics:'a2'},{songName:'a',singer:'a1',lyrics:'a2'},{songName:'a',singer:'a1',lyrics:'a2'}],
      songs: [{title:'True Love',artist:'James',lyrics:["Rich man, poor man, beggar or king,You just can't have everything.\n","So thank your stars above\n","For a song in your heart."]}],
      // songs:[],
      showCards: true,
      showErrorMsg: false,
      loading: false,
      queryTime: 1
    }
  }

  performSearch = (data, keySearchEnabled) => {
          const { query } = data

          this.setState({ loading: true, showErrorMsg: false }, async () => {

            try {
              const response = await API.get(
                  keySearchEnabled ? '/search/key/' + query + '/1':'/search/lyric/' + query + '/1'
              )
              console.log('response: ', response)
              console.log('response time: ', response.data.query_time)
              queryInfo.spellingCorrection = response.data.spellingCorrection
              this.setState({
                songs: response.data.songs,
                queryTime: response.data.query_time,
                showCards: true,
                loading: false
              })
              console.log('query: ', query)
              console.log('spellingCorrection: ', response.data.spellingCorrection)
            } catch (error) {
              // queryInfo.spellingCorrection="test"
              console.error(error)
              console.log('query: ', query)
              this.setState({
                showErrorMsg: true,
                loading: false
              })
            }
          })
        }

  render() {
    const { showCards, songs,showErrorMsg, loading, queryTime } = this.state

    return (
      <div>
       <ThemeProvider theme={theme}>
        <CssBaseline/>
          <AppBar position='relative'>
          <Toolbar>
          <LyricsOutlinedIcon className="icon" sx={{ fontSize: 40}}/>
            <Typography variant='h4' onClick={() => window.location.reload()}>
            <p style={{ fontFamily: "fantasy", marginTop: "20px", whiteSpace:"-moz-initial", textIndent:"0.8em"}}>
         
              Song Search
            </p>
            </Typography>

          </Toolbar>
          </AppBar>
     
          <div className="skeleton-card">
          <Container fixed>       
              <SearchInput
                performSearch={this.performSearch}
                showErrorMsg={showErrorMsg}
              />
              </Container>
            </div>
            <Fragment>
              {loading ?
                <Fragment>
                  {Array.apply(null, { length: 5 }).map((e, i) => (
                    <Skeleton variant="rect" width={790} height={0} className="skeleton-card" />
                  ))}
                </Fragment>
                : showCards && <Result performSearch={this.performSearch} data={songs} queryTime={queryTime} />
              }
            </Fragment>
            {/* showCards &&  <Result performSearch={this.performSearch} data={songs} queryTime={queryTime} /> */}
        </ThemeProvider>

        </div>
        
        
    )
  }
}