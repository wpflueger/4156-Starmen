/* istanbul ignore file */
import React, { useState, useEffect } from 'react'
import Autosuggest, {
	RenderSuggestion,
	RenderSuggestionsContainer,
	GetSuggestionValue,
	SuggestionsFetchRequested,
} from 'react-autosuggest'

import { Objects } from '../../utils'

import styles from './SuggestionInput.module.sass'

import 'react-datepicker/dist/react-datepicker.css'

interface SuggestionInputProps {
	label?: string
	value?: string
	required?: boolean
	className?: string
	containerClassName?: string
	suggestionLimit?: number
	selectOnChange?: boolean
	onSelect?: (value: any) => void
	onChange?: (value: any) => void
	/** A function to asynchronously provide suggestions to the input. */
	getSuggestions: (value: string) => Promise<any[]>
	/** Function to get the suggestion value from a list of suggestions. */
	getSuggestionValue?: GetSuggestionValue<any>
}

export const SuggestionInput = (props: SuggestionInputProps) => {
	const [text, setText] = useState('')
	const [suggestions, setSuggestions] = useState([] as any[])
	const [suggestionsMap, setSuggestionsMap] = useState({} as any)

	const getSuggestionValue = (v: any) => {
		if (props.getSuggestionValue) {
			return props.getSuggestionValue(v)
		}
		return v
	}

	const onChange = (nextText: string) => {
		if (props.selectOnChange && nextText && suggestions.length > 0) {
			const val = suggestionsMap[getSuggestionValue(nextText)]
			props.onSelect && props.onSelect(val)
		}
		setText(nextText)
		props.onChange && props.onChange(nextText)
	}

	const onSelect = (value: any) => {
		props.onSelect && props.onSelect(value)
		onChange(getSuggestionValue(value))
	}

	const renderSuggestion: RenderSuggestion<any> = (suggestion: any, { isHighlighted, query }) => {
		return (
			<div
				key={`${query}-${getSuggestionValue(suggestion)}`}
				onClick={() => {
					onSelect(suggestion)
					onSuggestionsClearRequested()
				}}
				className={`${styles.suggestion} ${isHighlighted ? styles.highlighted : ''}`}
			>
				{getSuggestionValue(suggestion)}
			</div>
		)
	}

	const renderSuggestionsContainer: RenderSuggestionsContainer = ({ containerProps, children, query }) => {
		containerProps.className = ''
		return (
			<div
				{...containerProps}
				className={styles.suggestions}
				style={{ opacity: suggestions.length > 0 ? '1' : '0' }}
			>
				{suggestions.map((s, i) => renderSuggestion(s, { isHighlighted: false, query: `${i}` }))}
			</div>
		)
	}

	const onSuggestionsFetchRequested: SuggestionsFetchRequested = (res) => {
		props.getSuggestions(res.value).then((s) => setSuggestions(s))
	}

	const onSuggestionsClearRequested = () => {
		setSuggestions([])
	}

	useEffect(() => {
		if (!Objects.isNullish(props.value)) {
			setText(props.value!)
		}
	}, [props.value])

	useEffect(() => {
		if (suggestions.length > 0) {
			const newSuggestionsMap = {} as any
			for (const suggestion of suggestions) {
				newSuggestionsMap[getSuggestionValue(suggestion)] = suggestion
			}
			setSuggestionsMap(newSuggestionsMap)
		}
	}, [suggestions])

	return (
		<div className={props.containerClassName}>
			{props.label && (
				<div>
					{props.label}
					{props.required && <span className={'color-quaternary'}> *</span>}
				</div>
			)}
			<Autosuggest
				suggestions={suggestions}
				onSuggestionsFetchRequested={onSuggestionsFetchRequested}
				onSuggestionsClearRequested={onSuggestionsClearRequested}
				renderSuggestionsContainer={renderSuggestionsContainer}
				getSuggestionValue={getSuggestionValue}
				renderSuggestion={renderSuggestion}
				inputProps={{
					onChange: (_, res) => onChange(res.newValue),
					value: text,
					className: `${styles.suggestion_input} ${suggestions.length !== 0 ? styles.no_bottom_border : ''}`,
				}}
			/>
		</div>
	)
}
