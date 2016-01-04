//Optional Services
(function(__myglobal){
	var ServiceTypes = Object.keys(opsvTmpl);
	var classNames = window.classNames;

	var OsLi = React.createClass({
		propTypes: {
			variant: React.PropTypes.object
		},
		render: function(){
			var cls = classNames({
				'selected': this.props.index === this.props.active
			});
			return (
				<li
					onClick={this.props.updateState} 
					className={cls} 
					ppid={this.props.variant.ppid} 
					lstPrice={this.props.variant.lstPrice}>
					{this.props.variant.vName + " Hours"}
				</li>
			)
		}
	});

	var OsUl = React.createClass({
		propTypes: {
			dat: React.PropTypes.object
		},
		updateState: function(index){
			this.props.updateState(index);
			ReactDOM.findDOMNode(this).blur();
		},
		render: function(){
			var ctx = this;
			var cls = classNames({
				'opt_serv_dropdown': true,
				'selected': ctx.props.active > -1
			});
			return (
				<ul tabIndex="-1" className={cls}>
				<li>Choose One</li>
				{this.props.dat.variants.map(function(v, i){
					return <OsLi index={i} active={ctx.props.active} updateState={ctx.updateState.bind(ctx, i)} key={v.ppid} variant={v} />
				})}
				</ul>
			)
		}
	});

	var OsDiv = React.createClass({
		render: function(){
			var ctx = this;
			return (
				<div className="other_service col-xs-6 col-sm-3">
					<header>{this.props.title}</header>
					<p>{this.props.dat.description}</p>
					{getPriceTag()}
					<OsUl 
					    active={this.props.active}
						dat={this.props.dat}
						updateState={this.props.updateState}/>
					<br style={{'clear':'both'}}/>
				</div>
			)

			function getPriceTag(){
				if (!isRSA) {
					return;
				} else {
					return (<span className="opt_serv_price">${parseFloat(ctx.props.price).toFixed(2)}</span>);
				}				
			}
		}
	});

	var OsCon = React.createClass({
		updateState: function(key, v){
			var stateChange = {};
			stateChange[key] = v;

			var servicesObj = opsvTmpl[key].variants[v];
			__myglobal.summary.removeOptional(opsvTmpl[key].variants[this.state[key]]);
			__myglobal.summary.addOptional(servicesObj);
			__myglobal.UnsetRecomm();
			this.setState(stateChange);
		},
		componentWillMount: function(){
			var ctx = this;
			Object.keys(this.state).forEach(function(v){
				__myglobal[v] = {};
				__myglobal[v].setState = function(s){					
					ctx.updateState(v,s);
				};
				__myglobal[v].getState = function(){
					return ctx.state[v];
				};
			});
		},
		getInitialState: function(){			
			return ServiceTypes.reduce(function(prev, curr){
				prev[curr] = -1;
				return prev;
			}, {});
		},
		render: function(){
			var ctx = this;
			return (
				<div>
					{ServiceTypes.map(function(v){
					return ( 
						<OsDiv 
						    key={v} 
							active={ctx.state[v]}
							dat={opsvTmpl[v]} 
							price={ !!opsvTmpl[v].variants[ctx.state[v]] ? opsvTmpl[v].variants[ctx.state[v]].lstPrice : '0'}
							title={v} 
							updateState={ctx.updateState.bind(ctx, v)}>
						</OsDiv>
					)
					})}
				</div>
			)
		}
	});

	ReactDOM.render(
		React.createElement(OsCon),
		document.getElementById('os_container')
	);
})(__rsGlobal);

