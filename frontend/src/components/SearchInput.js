import React, { Component} from 'react'
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';


import PropTypes from 'prop-types'
import { FormControlLabel, Typography, Checkbox } from '@mui/material'
// import { Autocomplete } from '@mui/material'
import API from './API.js'

import './SearchInput.css'

export default class SearchInput extends Component {
  constructor(props) {
    super(props)

    this.state = {
      query: '',
      keySearchEnabled: false,
      invalidMessage: '',
      suggestions: []
    }
  }

  componentDidMount() {
    this.setState({ showErrorMsg: false, invalidMessage: '' })
  }

  onSearchChange = e => {
    const query = e.target.value

    this.setState({ query }, async () => {
      if (query.length && /(\w+)\s$/.test(query)) {
        this.querySuggestion(query)
      } else if (!query.length) {
        this.setState({ suggestions: [] })
      }
    })
  }

  querySuggestion = async query => {
    const response = await API.get(`/query_suggest?query=${query}`)
    console.log('response', response)
    this.setState({ suggestions: response.data.results })
  }

  setSearchInput = (event) => {
    this.setState({ query: event.target.text }, this.lyricsSearch)
  }

  selectSearch = e => {
    e && e.preventDefault()
    const { query } = this.state
    console.log("test2")
    this.props.performSearch({query}, this.state.keySearchEnabled)
  }


  keySearch = e => {
    const { query } = this.state
    const keySearchEnabled = e.target.checked
  //打勾
    this.setState({ keySearchEnabled }, () => {
      if (query.length) {
        console.log("test1")
        this.props.performSearch({query}, keySearchEnabled)
      }
    }
    )
  }

    render(){
        const { keySearchEnabled, invalidMessage, suggestions } = this.state
        const { showErrorMsg } = this.props
        console.log(suggestions)

        return(
          <div className='search-form'>
            <br/>
            <br/>
            <Paper
            component="form" onSubmit={this.selectSearch}
            sx={{ p: '8px 4px', display: 'flex', alignItems: 'center', width: 700 }}>
            <InputBase onChange={this.onSearchChange}
            sx={{ ml: 2, flex: 1 }}
            placeholder={keySearchEnabled ? 'Search for keywords in a song...' : 'Search for song lyrics...'}
            inputProps={{ 'aria-label': 'search google maps' }}
            />
            <IconButton type="submit" sx={{ p: '10px' }} aria-label="search">
            <SearchIcon />
            </IconButton>
            </Paper>


            <FormControlLabel className="song-search"
              control={
                <Checkbox
                  checked={keySearchEnabled}
                  onChange={this.keySearch}
                  style ={{
                     color: "#FFFFFF",
                    }}
                  inputProps={{ 'aria-label': 'primary checkbox' }}
                />
              }
              label={<Typography style={{ color: '#FFFFFF' }}>Search for keywords</Typography>}
            />
          </div>       
        )
    }
}

SearchInput.propTypes = {
  performSearch: PropTypes.func.isRequired,
  showErrorMsg: PropTypes.bool.isRequired
}