import React from 'react'
import { Grid, Typography, Pagination ,Button,Link} from '@mui/material'
import PropTypes from 'prop-types'
import SongCard from './SongCard.js'
import './Result.css'
import queryInfo from './globalData';

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
            {queryInfo.spellingCorrection!=="" &&
            <div>
              <Grid container spacing={6}>
              <Typography variant="body1" >{`Do you mean:`}</Typography>
              <Link
              component="button"
              variant="body1"
              color="primary"
              onClick={() => {
                queryInfo.query=queryInfo.spellingCorrection;
                queryInfo.spellingCorrection="";
                this.props.performSearch(queryInfo.query, queryInfo.keySearchEnabled)                
              }}
              >
              {queryInfo.spellingCorrection}
              </Link>
              </Grid>
              <Typography variant="body1" >{`Your current search is ${queryInfo.query}`}</Typography>
            </div>
            }

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
  performSearch: PropTypes.func.isRequired,
  data: PropTypes.array.isRequired,
  queryTime: PropTypes.number.isRequired
}
