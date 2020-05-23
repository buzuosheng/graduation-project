import React from 'react';
import './App.css';
import { useState } from 'react';
import qr from './qr.png'
import fetch from 'unfetch'
import useSWR from 'swr';

const App: React.FC = () => {

  const fetcher = (url: string) =>
    fetch(url,)
      .then(r => r.json())

  const { data } = useSWR('http://localhost:7001/tv', fetcher)

  function Getmovie () {
    const i = Math.ceil(Math.random() * 100) - 1
    setMovie(data[i])
  }

  const init = {
    title: '地球脉动 第二季 Planet Earth Season 2(2016)',
    img: 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2410512421.jpg',
    directorr: '伊丽莎白·怀特/贾斯汀·安德森/艾玛·纳珀',
    actor: '大卫·爱登堡',
    rate: '9.9'
  }

  const [movie, setMovie] = useState(init)

  return (
    <div>
      {/* <Helmet>
        <title>时间戳转换 - 前端武器库</title>
        <meta name='description' content='时间戳在线转换' />
        <meta name='keywords' content='时间,时间戳,在线工具,转换' />
      </Helmet> */}
      <div className = 'header'></div>
      <div className = 'movie_main'>
        <img height = {300} width = {200} alt = {movie.title} src = {movie.img} />
        <p>{ '《' + movie.title + '》' }</p>
        <p>{ movie.directorr || '' }</p>
        <p>{ movie.actor || '' }</p>
        <p>{ movie.rate || '' }</p>
        <button onClick = { Getmovie }>
          换一部
        </button>
        <p>截屏分享</p>
        <img alt = '截屏分享' height = {40} width = {40} src = {qr} />
      </div>
    </div>
  )
}

export default App