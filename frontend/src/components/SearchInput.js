import React, { Component} from 'react'
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import queryInfo from './globalData';

import PropTypes from 'prop-types'
import { FormControlLabel, Typography, Checkbox, Button } from '@mui/material'
import { Autocomplete } from '@mui/material'
import TextField from '@mui/material/TextField'
import API from './API.js'

import './SearchInput.css'

export default class SearchInput extends Component {
  constructor(props) {
    super(props)

    this.state = {
      query: '',
      keySearchEnabled: false,
      invalidMessage: '',
      suggestions: ['I','I love','I love you']
    }
  }

  componentDidMount() {
    this.setState({ showErrorMsg: false, invalidMessage: '' })
  }

  onSearchChange = e => {
    const query = e.target.value

    this.setState({ query }, async () => {
      if (query.length && /(\w+)\s$/.test(query)) {
      // if (query.length) {
        // && /(\w+)\s$/.test(query)
        console.log('suggest', query)
        this.querySuggestion(query)
      } else if (!query.length) {
        this.setState({ suggestions: [] })
      }
    })
  }

  querySuggestion = async query => {
    // const response = await API.get(`/query_suggest?query=${query}`)
    const response = await API.get('/suggest/'+query)
    console.log('response suggestion', response)
    this.setState({ suggestions: response.data.results })
  }

  setSearchInput = (event) => {
    this.setState({ query: event.target.text }, this.lyricsSearch)
  }

  selectSearch = e => {
    e && e.preventDefault()
    const { query } = this.state
    queryInfo.query=query;
    queryInfo.keySearchEnabled=this.state.keySearchEnabled;
    this.props.performSearch({query}, this.state.keySearchEnabled)
  }


  keySearch = e => {
    const { query } = this.state
    const keySearchEnabled = e.target.checked
  //打勾
    this.setState({ keySearchEnabled }, () => {
      if (query.length) {
        queryInfo.query=query;
        queryInfo.keySearchEnabled=this.state.keySearchEnabled;
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
          <form noValidate autoComplete="off" onSubmit={this.selectSearch}>
          <div className='search-form'>
            <br/>
            <br/>

              <Autocomplete
                disablePortal
                id="combo-box-demo"
                options={suggestions}
                autoComplete
                includeInputInList
                disableListWrap
                disableOpenOnFocus
                freeSolo
                sx={{ width: 700}}

                onChange={(e)=>{
                  console.log(e.target.value);
                }}
                renderInput={(params) => {
                  return(
                    <TextField
                      {...params}
                      label={keySearchEnabled ? 'Search for keywords in a song...' : 'Search for song lyrics...'}
                      variant="outlined"
                      fullWidth
                      onChange={this.onSearchChange}
                    />
                  )}}

                  

              
              />


            <IconButton type="submit" sx={{ p: '10px', color: 'darkgrey'}} aria-label="search">
            <SearchIcon />
            </IconButton>
           

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
          </form>    
        )
    }
}

SearchInput.propTypes = {
  performSearch: PropTypes.func.isRequired,
  showErrorMsg: PropTypes.bool.isRequired
}