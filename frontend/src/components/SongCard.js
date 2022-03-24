import React from 'react'
import PropTypes from 'prop-types'
import { Card, CardMedia, Box, CardContent, CardActionArea, Typography,IconButton } from '@mui/material'
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import './SongCard.css'

const lYRICS_LIMIT = 200
const imgSrc=["thumb1.jpg","thumb2.jpeg","thumb3.jpeg","thumb4.jpeg","thumb5.jpeg","thumb6.jpg","thumb7.jpg","thumb8.jpg","thumb9.jpg","thumb10.jpg","thumb11.jpg","thumb12.jpg","thumb13.jpg","thumb14.jpg","thumb15.jpg"]


export default class SongCard extends React.Component {
  render() {
    let { title,artist,lyrics_3 } = this.props
    var r=Math.floor(Math.random() * 14)
    return (
      <div>
        <Card  sx={{ display: 'flex' }} className="card-container">
        <CardMedia
          className="card-media"
          component="img"
          sx={{ width: 200, height:200 }}
          image={require(`../static/images/${imgSrc[r]}`)}
          alt="Live from space album cover"
          />
          <Box sx={{ display: 'flex', flexDirection: 'column' }}> 
            <div className="card-content">
              <CardContent sx={{ flex: '1 0 auto' }}>
                <Typography variant="h6">{title}</Typography>
                <br/>
                <Typography variant="body2">{artist}</Typography>
                <br/>
                <IconButton aria-label="play/pause" onClick={() => {window.location.href="https://open.spotify.com/search/"+title}}>
                <PlayArrowIcon sx={{ height: 38, width: 38 }} />
                </IconButton>
              </CardContent>
            </div>
            </Box>
          <Box sx={{ display: 'flex', flexDirection: 'column' }}> 
          <div className="card-lyrics">
              <CardContent>
              <view className='DetailsTitle'>{lyrics_3}</view>
              </CardContent>
            </div>
            </Box>
        </Card>
      </div>
    )
  }
}

SongCard.propTypes = {
  song: PropTypes.shape({
    title: PropTypes.string.isRequired,
    artist: PropTypes.string.isRequired,
    lyrics_3: PropTypes.string.isRequired,
  })
}
    // lyrics_3: PropTypes.array.isRequired,
    // lyrics: PropTypes.string.isRequired,
    // pos: PropTypes.number.isRequired