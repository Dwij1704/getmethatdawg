# Bash completion for getmethatdawg
_getmethatdawg_complete() {
    local cur prev words cword
    _init_completion || return

    case $prev in
        getmethatdawg)
            COMPREPLY=( $(compgen -W "deploy --help --version" -- "$cur") )
            return
            ;;
        deploy)
            # Complete with Python files in current directory
            COMPREPLY=( $(compgen -f -X "!*.py" -- "$cur") )
            return
            ;;
        *.py)
            COMPREPLY=( $(compgen -W "--auto-detect --name --region --requirements" -- "$cur") )
            return
            ;;
        --name)
            # No completion for app name
            return
            ;;
        --region)
            COMPREPLY=( $(compgen -W "iad ord sjc fra nrt hkg syd" -- "$cur") )
            return
            ;;
        --requirements)
            # Complete with txt files
            COMPREPLY=( $(compgen -f -X "!*.txt" -- "$cur") )
            return
            ;;
    esac

    case $cur in
        -*)
            COMPREPLY=( $(compgen -W "--help --version --auto-detect --name --region --requirements" -- "$cur") )
            ;;
        *)
            if [[ ${words[1]} == "deploy" ]]; then
                # Complete with Python files for deploy command
                COMPREPLY=( $(compgen -f -X "!*.py" -- "$cur") )
            else
                COMPREPLY=( $(compgen -W "deploy --help --version" -- "$cur") )
            fi
            ;;
    esac
}

complete -F _getmethatdawg_complete getmethatdawg 