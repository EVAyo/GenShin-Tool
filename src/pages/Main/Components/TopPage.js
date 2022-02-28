import { SPEED_CHANGERS } from "appConfig"
import Memoized from "components/Memoized";
import { FaSyncAlt, FaStop } from "react-icons/fa";
import { memo, useEffect, useState, useRef } from "react";
import { SongStore } from "stores/SongStore";
import { SliderStore } from "stores/SongSliderStore";
import { observe } from "mobx";
import { BsTriangleFill } from "react-icons/bs";
import './Track.css'
import { AppButton } from "components/AppButton";
export default memo(function TopPage({ restart, handleSpeedChanger, speedChanger, approachingScore, hasSong }) {
    const [sliderState, setSliderState] = useState(SliderStore.state.data)
    const [songData, setSongData] = useState(SongStore.state.data)
    const [selectedThumb, setSelectedThumb] = useState(null)
    const [inputDimension, setInputDimension] = useState({})
    const thumb1 = useRef()
    const thumb2 = useRef()
    const slider = useRef()
    useEffect(() => {
        const dispose = observe(SliderStore.state, (newState) => {
            setSliderState(newState.object.data)
        })
        const dispose2 = observe(SongStore.state, (newState2) => {
            setSongData(newState2.object.data)
        })
        return () => {
            dispose();
            dispose2()
        }
    }, [])
    
    useEffect(() => {
        if (selectedThumb === null) return
        function resetSelection() {
            if (selectedThumb !== null) setSelectedThumb(null)
        }
        window.addEventListener('pointerup', resetSelection)
        window.addEventListener('blur', resetSelection)
        return () => {
            window.removeEventListener('pointerup', resetSelection)
            window.removeEventListener('blur', resetSelection)
        }
    }, [selectedThumb])

    const handleSliderClick = (event) => {
        const size = slider.current.getBoundingClientRect()
        const x = event.clientX
        const thumb1X = thumb1.current.getBoundingClientRect().x
        const thumb2X = thumb2.current.getBoundingClientRect().x
        const left = Math.abs(thumb1X - x)
        const right = Math.abs(thumb2X - x)
        setInputDimension(size)
        const currentThumb = left >= right ? 'right' : 'left'
        setSelectedThumb(left >= right ? 'right' : 'left')
        handleSliderMove(event, currentThumb)
    }
    const handleSliderLeave = (event) => {
        setSelectedThumb(null)
    }
    const handleSliderMove = (event, override) => {
        if (selectedThumb === null && !override) return
        const currentThumb = override || selectedThumb
        const sliderX = inputDimension.x
        const sliderWidth = inputDimension.width
        const x = event.clientX - sliderX
        let value = Math.round(x / sliderWidth * sliderState.size)
        if(value < 0) value = 0
        if(value > sliderState.size) value = sliderState.size
        if (currentThumb === 'left') {
            if (value - sliderState.end < -1) SliderStore.setPosition(value)
        } else {
            if (value - sliderState.position > 1) SliderStore.setState({ end: value })
        }
    }
    const left = sliderState.size !== 0 ? sliderState.position / sliderState.size * 100 : 0
    const right = sliderState.size !== 0 ? sliderState.end / sliderState.size * 100 : 100
    return <div className="upper-right" style={!hasSong ? { display: 'none' } : {}} >
        {songData.eventType === 'approaching' &&
            <Score data={approachingScore} />
        }
        <div className="slider-wrapper">
            <AppButton className="slider-button" onClick={SongStore.reset}>
                <Memoized>
                    <FaStop />
                </Memoized>
            </AppButton>
            <div
                className="slider-outer"
                ref={slider}
                onPointerUp={handleSliderLeave}
                onPointerMove={handleSliderMove}
                onPointerDown={handleSliderClick}
            >
                <div className="slider-full">
                    <div className="slider-current" style={{ width: `${sliderState.current / sliderState.size * 100}%` }} />
                </div>
                <div className="two-way-slider">
                    <div className="two-way-slider-thumb" style={{ marginLeft: `calc(${left}% - 8px)` }} ref={thumb1}>
                        <BsTriangleFill width={16} style={{filter: 'drop-shadow(rgba(0, 0, 0, 0.4) 0px 2px 2px)'}}/>
                        <div style={{ fontSize: '0.8rem' }}>
                            {sliderState.position}
                        </div>
                    </div>
                    <div className="two-way-slider-thumb" style={{ marginLeft: `calc(${right}% - 8px)` }} ref={thumb2}>
                        <BsTriangleFill width={16} style={{filter: 'drop-shadow(rgba(0, 0, 0, 0.4) 0px 2px 2px)'}}/>
                        <div style={{ fontSize: '0.8rem' }}>
                            {sliderState.end}
                        </div>
                    </div>
                </div>
            </div>

            <AppButton className="slider-button" onClick={restart}>
                <Memoized>
                    <FaSyncAlt />
                </Memoized>
            </AppButton>
            <select
                className='slider-select'
                onChange={handleSpeedChanger}
                value={speedChanger.name}
            >
                <option disabled>Speed</option>
                {SPEED_CHANGERS.map(e => {
                    return <option value={e.name} key={e.name}>
                        {e.name}
                    </option>
                })}
            </select>
        </div>
    </div>
}, (prev, next) => {
    return prev.speedChanger === next.speedChanger
        && prev.approachingScore === next.approachingScore && prev.hasSong === next.hasSong
})


function Score(props) {
    const { combo, score, correct, wrong } = props.data
    return <div className='approaching-accuracy'>
        <table>
            <tbody>
                <tr>
                    <td className='sc-2'>Accuracy</td>
                    <td className='sc-1'>{(correct / (correct + wrong - 1) * 100).toFixed(1)}%</td>
                </tr>
                <tr>
                    <td className='sc-2'>Score</td>
                    <td className='sc-1'>{score}</td>
                </tr>
                <tr>
                    <td className='sc-2'>Combo</td>
                    <td className='sc-1'>{combo}</td>
                </tr>
            </tbody>
        </table>
    </div>
}
