import React from 'react'
import { Grid, Typography, Pagination } from '@mui/material'
import PropTypes from 'prop-types'
import SongCard from './SongCard.js'
import API from './API.js'
import './Result.css'

export default class Result extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      data: [],
      songId: null,
      errorSongInfoMsg: '',
      songInfo: {},
      offset: 1,
      perPage: 10,
      count: 0
    }
  }
  componentDidMount() {
    this.setState({ data: this.props.data })
    let count = Math.ceil(this.props.data.length / this.state.perPage)
    console.log(count, "count")
    this.setState({ count: count })
  }
  handleClick = (offset) => {
    console.log(offset, 'offset')
    this.setState({ offset: offset })
  }
  render() {
    const count = this.state.count
    const { data, offset, perPage } = this.state
    const { queryTime } = this.props
    const time = (Math.round(queryTime * 100) / 100).toFixed(3)
    return (
      <div className="result-container">
        <Grid container spacing={6}>
          <Grid item xs={8}>
            {data.length > 0 &&
            <Typography variant="body1" className="query-results">{`Query results: ${data.length} songs (${time} seconds)`}</Typography>
            }
            {data.length > perPage &&
              <Pagination
                limit={perPage}
                offset={offset}
                count={count}
                color="primary"
                onChange={(e, offset) => this.handleClick(offset)}
              />
            }
            {data.slice((offset - 1) * perPage, offset * perPage).map((song, idx) =>
              <SongCard key={idx} {...song} />
            )}
          </Grid>
        </Grid>
      </div>
    )
  }
}
Result.propTypes = {
  data: PropTypes.array.isRequired,
  queryTime: PropTypes.number.isRequired
}
